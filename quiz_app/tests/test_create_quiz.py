import pytest
import time
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from requests.exceptions import Timeout, RequestException

MAX_RETRIES = 5
RETRY_DELAY = 5

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
    
    api_client.cookies['access_token'] = response.cookies.get('access_token').value
    return api_client

@pytest.fixture
def quiz_url():
    """Fixture for the quiz creation URL."""
    return reverse('create-quiz')

def post_with_retry(api_client, url, data, retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Helper function to perform POST requests with retry logic."""
    for attempt in range(retries):
        try:
            response = api_client.post(url, data, format='json', timeout=30)
            return response
        except Timeout:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                pytest.fail("The service did not respond after multiple attempts.")
        except RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                pytest.fail(f"Request failed after multiple attempts: {str(e)}")
    return None

@pytest.mark.django_db
def test_create_quiz(api_client, login_user, quiz_url):
    """Test creating a quiz with a valid URL."""
    data = {
        "url": "https://www.youtube.com/watch?v=u-buCC1LWr8"
    }
    response = post_with_retry(api_client, quiz_url, data)
    
    assert response is not None, "The request failed."
    assert response.status_code == status.HTTP_201_CREATED
    
    expected_fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
    for field in expected_fields:
        assert field in response.data

@pytest.mark.django_db
def test_create_quiz_with_invalid_url(api_client, login_user, quiz_url):
    """Test creating a quiz with an invalid URL."""
    data = {
        "url": "https://www.youtube.com/watch?v=u-LWr8"
    }
    response = post_with_retry(api_client, quiz_url, data)
    
    assert response is not None, "The request failed."
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_quiz_without_login(api_client, quiz_url):
    """Test creating a quiz without being logged in (should return 401 Unauthorized)."""
    api_client.cookies['access_token'] = ""
    data = {
        "url": "https://www.youtube.com/watch?v=u-buCC1LWr8"
    }
    response = post_with_retry(api_client, quiz_url, data)
    
    assert response is not None, "The request failed."
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_create_quiz_with_empty_url(api_client, login_user, quiz_url):
    """Test creating a quiz with an empty URL (should return 400 Bad Request)."""
    data = {
        "url": ""
    }
    response = post_with_retry(api_client, quiz_url, data)
    
    assert response is not None, "The request failed."
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

@pytest.mark.django_db
def test_create_quiz_invalid_url_format(api_client, login_user, quiz_url):
    """Test creating a quiz with a malformed URL (should return 400 Bad Request)."""
    data = {
        "url": "invalid-url"
    }
    response = post_with_retry(api_client, quiz_url, data)
    
    assert response is not None, "The request failed."
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
