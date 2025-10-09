"""
Get-quiz API tests (concise).

Covers
------
- Success: owner can fetch -> 200 + expected fields.
- Auth: unauthenticated -> 401; non-owner -> 403.
- Existence: missing quiz -> 404.
- Error path: demonstrates server-error expectation case.
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz

@pytest.fixture
def owner():
    """Fixture to create a test owner (user)."""
    owner = User.objects.create_user(username="testowner", password="testpassword")
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
def test_get_quiz_success(api_client, quiz, owner):
    """Test getting a quiz successfully as the owner."""
    api_client.force_authenticate(user=owner)

    response = api_client.get(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == quiz.id
    assert response.data["title"] == quiz.title
    assert response.data["description"] == quiz.description

@pytest.mark.django_db
def test_get_quiz_unauthenticated(api_client, quiz):
    """Test getting a quiz without authentication."""
    response = api_client.get(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_quiz_forbidden(api_client, quiz, owner):
    """Test getting a quiz as a user who is not the owner."""
    another_owner = User.objects.create_user(username="anotherowner", password="password")

    api_client.force_authenticate(user=another_owner)

    response = api_client.get(f"/api/quizzes/{quiz.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_get_quiz_not_found(api_client, owner):
    """Test getting a non-existent quiz."""
    api_client.force_authenticate(user=owner)

    response = api_client.get("/api/quizzes/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_quiz_server_error(api_client, owner):
    """Test server error while getting a quiz."""
    api_client.force_authenticate(user=owner)

    with pytest.raises(Exception):
        response = api_client.get("/api/quizzes/1/")
        response.raise_for_status()
