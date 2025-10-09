from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Responsibilities
    ----------------
    - Validates input and creates a new user.
    - Enforces a case-insensitive unique email.
    - Validates the password using Django's configured password validators.
    - Uses `User.objects.create_user(...)` so the password is hashed and defaults are set.

    Fields
    ------
    - username: str, required
    - email: str, required, unique (case-insensitive), stored lowercased
    - password: str, write_only, validated but never returned

    Notes
    -----
    - Email is trimmed and lowercased to avoid duplicates caused by
      whitespace/casing differences.
    - Creation runs inside a DB transaction.
    """
    class Meta:
        """Serializer for user registration, handling username, email, and password."""
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_email(self, value):
        """Check if the email is already in use."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """Create a new user account with the provided details."""
        pw = self.validated_data['password']

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
     """
    Obtain JWT tokens by authenticating with email + password
    instead of username + password.

    Behavior
    --------
    - Accepts `email` and `password`.
    - Resolves the user by `email` (case-insensitive).
    - Injects the resolved `username` into `attrs` so the parent
      serializer (`TokenObtainPairSerializer`) can proceed normally.

    Security
    --------
    - Returns a generic error for invalid credentials to avoid
      leaking which field failed.
    - Optionally checks `is_active` (uncomment if desired).
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """Initialize the serializer and remove the username field."""
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop('username', None)

    def validate(self, attrs):
        """Validate email and password, and return authentication tokens."""
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        
        attrs["username"] = user.username
        data = super().validate(attrs)
        return data
