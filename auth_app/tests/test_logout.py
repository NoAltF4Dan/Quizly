"""
Logout API tests (concise).

Covers
------
- Success: valid access token -> 200 with success detail; token becomes unusable (subsequent request -> 401).
- Failure: invalid token on logout -> 401.

Fixtures
--------
- user: test user.
- api_client: DRF API client.
- login_user: logs in, stores access token cookie, returns (client, token).
- logout_url: reverse('token-blacklist').
"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

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
    from rest_framework.test import APIClient
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
def logout_url():
    """Fixture for the logout URL."""
    return reverse('token-blacklist')

@pytest.mark.django_db
def test_logout_success(api_client, login_user, logout_url):
    """Test logging out successfully with a valid token and ensuring the token is blacklisted."""
    api_client, access_token = login_user

    response = api_client.post(
        logout_url,
        {},
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
    }

    response = api_client.get(
        logout_url,
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_invalid_token(api_client, user, logout_url):
    """Test logging out with an invalid token (after logout)."""
    invalid_token = 'invalidtoken'

    response = api_client.post(
        logout_url,
        {},
        HTTP_AUTHORIZATION=f'Bearer {invalid_token}'
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED