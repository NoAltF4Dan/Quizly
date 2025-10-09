"""
Refresh-token API tests (concise).

Covers
------
- Success: refresh with valid cookies -> new access token issued.
- Missing cookie: no access/refresh cookie -> 400/401.
- Invalid refresh: bogus refresh cookie -> 401.

Fixtures
--------
- user, api_client, login_user: helper setup for authenticated client.
- refresh_url: reverse('token-refresh').
"""

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
        password='testpassword123',
        email='test@test.de'
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
        'password': 'testpassword123'
    }, format='json')
    
    access_token = response.cookies.get('access_token').value
    api_client.cookies['access_token'] = access_token
    return api_client, access_token

@pytest.fixture
def refresh_url():
    """Fixture for the refresh token URL."""
    return reverse('token-refresh')

@pytest.mark.django_db
def test_refresh_token_success(api_client, login_user, refresh_url):
    """Test refreshing the token successfully with a valid refresh request."""
    api_client, access_token = login_user

    response = api_client.post(refresh_url, {}, format='json')

    new_access_token = response.cookies['access_token'].value
    
    assert access_token != new_access_token
    
    assert response.json() == {
        "detail": "Token refreshed",
        "access": "new_access_token"
    }

@pytest.mark.django_db
def test_refresh_token_without_cookie(api_client, refresh_url):
    """Test refreshing the token without providing the access token cookie."""
    client = APIClient()

    response = client.post(refresh_url, {}, format='json')

    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

@pytest.mark.django_db
def test_refresh_token_invalid_refresh_token(api_client, refresh_url):
    """Test refreshing the token with an invalid refresh token."""
    client = APIClient()
    client.cookies['refresh_token'] = 'invalid_refresh_token'

    response = client.post(refresh_url, {}, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED