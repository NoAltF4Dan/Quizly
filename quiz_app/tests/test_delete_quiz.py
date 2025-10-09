"""
Delete-quiz API tests (concise).

Covers
------
- Success: owner can delete -> 204 and DB record removed.
- Auth: unauthenticated -> 401; non-owner -> 403.
- Existence: deleting missing quiz -> 404.

Fixtures
--------
- owner: test user owning the quiz.
- quiz: quiz instance linked to owner.
- api_client: DRF API client.
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock
from django.contrib.auth.models import User
from quiz_app.models import Quiz

@pytest.fixture
def owner():
    """Fixture to create a test owner (user)."""
    owner = User.objects.create_user(username="owneruser", password="ownerpassword")
    return owner

@pytest.fixture
def quiz(owner):
    """Fixture to create a test quiz associated with an owner."""
    quiz = Quiz.objects.create(
        title="Test Quiz",
        description="This is a test quiz.",
        owner=owner
    )
    return quiz

@pytest.fixture
def api_client():
    """Fixture to return an instance of APIClient."""
    return APIClient()

@pytest.mark.django_db
def test_delete_quiz_success(api_client, quiz, owner):
    """Test successful deletion of a quiz by the owner."""
    api_client.force_authenticate(user=owner)

    response = api_client.delete(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(Quiz.DoesNotExist):
        Quiz.objects.get(id=quiz.id)

@pytest.mark.django_db
def test_delete_quiz_unauthenticated(api_client, quiz):
    """Test deleting a quiz without authentication."""
    response = api_client.delete(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_delete_quiz_forbidden(api_client, quiz, owner):
    """Test deleting a quiz by a user who is not the owner."""
    another_user = User.objects.create_user(username="anotheruser", password="password")

    api_client.force_authenticate(user=another_user)

    response = api_client.delete(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_quiz_not_found(api_client, owner):
    """Test deleting a non-existent quiz."""
    api_client.force_authenticate(user=owner)

    response = api_client.delete("/api/quizzes/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND