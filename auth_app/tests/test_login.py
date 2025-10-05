import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

@pytest.fixture
def create_user(db):
    """Fixture to create a user with default or custom username and password."""
    def make_user(username='newuser', password='newpassword123'):
        return User.objects.create_user(
            username=username,
            password=password,
            email='newuser@test.de'
        )
    return make_user


@pytest.fixture
def login_url():
    """Fixture for the login URL."""
    return reverse('login-view')


@pytest.fixture
def user_data():
    """Fixture for the user login data."""
    return {
        'username': 'newuser',
        'password': 'newpassword123',
    }


@pytest.mark.django_db
def test_login(client, create_user, login_url, user_data):
    """Test successful login with correct credentials."""
    user = create_user()
    response = client.post(login_url, user_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.cookies
    assert 'refresh_token' in response.cookies
    assert response.json() == {
        "detail": "Login successfully!",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@pytest.mark.django_db
def test_login_false_username(client, create_user, login_url, user_data):
    """Test login attempt with an incorrect username."""
    create_user()
    data = {
        'username': 'michwirdesniegeben',
        'password': user_data['password']
    }
    response = client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access_token' not in response.cookies
    assert 'refresh_token' not in response.cookies
    assert response.json() == {
        "detail": "No active account found with the given credentials"
    }


@pytest.mark.django_db
def test_login_false_password(client, create_user, login_url, user_data):
    """Test login attempt with an incorrect password."""
    create_user()
    data = {
        'username': user_data['username'],
        'password': 'somepassword'
    }
    response = client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access_token' not in response.cookies
    assert 'refresh_token' not in response.cookies
    assert response.json() == {
        "detail": "No active account found with the given credentials"
    }


@pytest.mark.django_db
def test_login_missing_password(client, create_user, login_url, user_data):
    """Test login attempt with a missing password."""
    create_user()
    data = {
        'username': user_data['username'],
        'password': ''
    }
    response = client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'access_token' not in response.cookies
    assert 'refresh_token' not in response.cookies
    assert response.json() == {
        'password': ['This field may not be blank.']
    }


@pytest.mark.django_db
def test_login_missing_username(client, create_user, login_url, user_data):
    """Test login attempt with a missing username."""
    create_user()
    data = {
        'username': '',
        'password': user_data['password']
    }
    response = client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'access_token' not in response.cookies
    assert 'refresh_token' not in response.cookies
    assert response.json() == {
        'username': ['This field may not be blank.']
    }


@pytest.mark.django_db
def test_login_empty_request(client, login_url):
    """Test an empty request body."""
    response = client.post(login_url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'username': ['This field is required.'],
        'password': ['This field is required.']
    }
