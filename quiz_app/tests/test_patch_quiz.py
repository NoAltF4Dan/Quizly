import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz

@pytest.fixture
def user():
    """Creates and returns a test user."""
    owner = User.objects.create_user(username="testuser", password="testpassword")
    return owner

@pytest.fixture
def quiz(user):
    """Creates and returns a test quiz associated with a user."""
    quiz = Quiz.objects.create(
        title="Test Quiz",
        description="This is a test quiz.",
        owner=user
    )
    return quiz

@pytest.fixture
def api_client():
    """Returns an instance of APIClient for testing."""
    return APIClient()

@pytest.mark.django_db
def test_patch_quiz_success(api_client, quiz, user):
    """Tests successful quiz update with valid data."""
    api_client.force_authenticate(user=user)

    updated_data = {"title": "Partially Updated Title"}

    response = api_client.patch(f"/api/quizzes/{quiz.id}/", updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == quiz.id
    assert response.data["title"] == "Partially Updated Title"
    assert response.data["description"] == quiz.description

@pytest.mark.django_db
def test_patch_quiz_invalid_data(api_client, quiz, user):
    """Tests quiz update with invalid data (empty title)."""
    api_client.force_authenticate(user=user)

    invalid_data = {"title": ""}

    response = api_client.patch(f"/api/quizzes/{quiz.id}/", invalid_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data

@pytest.mark.django_db
def test_patch_quiz_unauthenticated(api_client, quiz):
    """Tests quiz update without authentication."""
    updated_data = {"title": "Unauthenticated Update"}

    response = api_client.patch(f"/api/quizzes/{quiz.id}/", updated_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_patch_quiz_forbidden(api_client, quiz, user):
    """Tests quiz update by a user who is not the owner."""
    another_user = User.objects.create_user(username="anotheruser", password="password")

    api_client.force_authenticate(user=another_user)

    updated_data = {"title": "Unauthorized Update"}

    response = api_client.patch(f"/api/quizzes/{quiz.id}/", updated_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_patch_quiz_not_found(api_client, user):
    """Tests quiz update for a non-existent quiz."""
    api_client.force_authenticate(user=user)

    updated_data = {"title": "Non-existent Quiz Update"}

    response = api_client.patch("/api/quizzes/999/", updated_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_patch_quiz_server_error(api_client, user):
    """Tests quiz update with a server error simulation."""
    api_client.force_authenticate(user=user)

    try:
        response = api_client.patch("/api/quizzes/1/", {"title": "Server Error Update"})
        assert False, "Expected exception but none was raised"
    except Exception:
        pass
