import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def user():
    """Fixture to create a test user."""
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='test@test.de'
    )


@pytest.fixture
def register_url():
    """Fixture to provide the registration URL."""
    return reverse('register-view')


@pytest.fixture
def api_client():
    """Fixture to return an instance of APIClient."""
    return APIClient()


@pytest.mark.django_db
def test_register(api_client, register_url):
    """Test registering a new user."""
    user_data = {
        'username': 'newuser',
        'password': 'newpassword123',
        'email': 'newuser@test.de'
    }
    
    response = api_client.post(register_url, user_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()
    assert response.json() == {
        "detail": "User created successfully!"
    }


@pytest.mark.django_db
def test_register_existing_username(api_client, register_url, user):
    """Test registering with an existing username."""
    data = {
        'username': 'testuser',
        'password': 'somepassword',
        'email': 'other@test.de'
    }
    
    response = api_client.post(register_url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.json()


@pytest.mark.django_db
def test_register_invalid_email(api_client, register_url):
    """Test registering with an invalid email."""
    data = {
        'username': 'newuser2',
        'password': 'newpassword123',
        'email': 'invalidemail'
    }
    
    response = api_client.post(register_url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.json()


@pytest.mark.django_db
def test_register_missing_fields(api_client, register_url):
    """Test registering with missing fields (e.g. no email or password)."""
    data = {
        'username': 'newuser3',
        'password': ''
    }
    
    response = api_client.post(register_url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.json()


@pytest.mark.django_db
def test_register_email_already_taken(api_client, register_url, user):
    """Test registering with an email that already exists."""
    data = {
        'username': 'newuser5',
        'password': 'newpassword123',
        'email': 'test@test.de'
    }
    
    response = api_client.post(register_url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.json()