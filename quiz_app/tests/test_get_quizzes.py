import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def user():
    """Fixture to create a test user."""
    return User.objects.create_user(
        username='newuser',
        password='newpassword123',
        email='newuser@test.de'
    )

@pytest.fixture
def api_client():
    """Fixture to return an instance of APIClient."""
    return APIClient()

@pytest.fixture
def login_user(api_client, user):
    """Fixture to log in a user and store the access token."""
    login_url = reverse('login-view')
    response = api_client.post(login_url, {
        'username': user.username,
        'password': 'newpassword123'
    }, format='json')
    
    access_token = response.cookies.get('access_token').value
    api_client.cookies['access_token'] = access_token
    return api_client, access_token

@pytest.fixture
def quiz_urls():
    """Fixture for the quiz-related URLs."""
    return {
        'quiz_create': reverse('create-quiz'),
        'quiz_list': reverse('quiz-list')
    }

@pytest.mark.django_db
def test_get_quizzes(api_client, login_user, quiz_urls):
    """Test getting the list of quizzes."""
    api_client, access_token = login_user
    
    response = api_client.get(quiz_urls['quiz_list'])
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_create_quiz(api_client, login_user, quiz_urls):
    """Test creating a new quiz."""
    api_client, access_token = login_user

    data = {
        "url": "https://www.youtube.com/watch?v=u-buCC1LWr8"
    }
    
    response = api_client.post(quiz_urls['quiz_create'], data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    
    expected_fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
    for field in expected_fields:
        assert field in response.data
