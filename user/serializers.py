from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from user.models import Profile


class RegistrationSerializer(serializers.Serializer):
    # required fields
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)

    # profile
    user_type = serializers.CharField(max_length=255)

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return username

    def validate_password(self, password):
        validate_password(password)
        return password

    def save(self):
        username = self.validated_data["username"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]

        # profile
        user_type = self.validated_data["user_type"]

        # Create the User object
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_active=True,
            )
        except Exception:
            raise serializers.ValidationError("Could not create user.")
        try:
            Profile.objects.get_or_create(user=user, user_type=user_type)
        except Exception:
            raise serializers.ValidationError("Could not create user profile.")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.get_user_type_display", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "first_name",
            "last_name",
            "email",
        )
