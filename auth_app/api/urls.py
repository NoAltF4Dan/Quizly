from django.urls import path
from .views import RegistrationView, CookieTokenObtainView, CookieRefreshView, TokenBlacklistView

"""URL configuration for handling user authentication processes including registration, login, logout, and token refresh using class-based views."""
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register-view'),
    path('login/', CookieTokenObtainView.as_view(), name='login-view'),
    path('logout/', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token-refresh'),
]
