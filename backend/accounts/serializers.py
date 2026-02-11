"""
Serializers for user registration, login, and profile management.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "company_name",
            "phone",
            "password",
            "password_confirm",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return data

    def validate_role(self, value):
        # Prevent users from registering as admin
        if value == User.Role.ADMIN:
            raise serializers.ValidationError(
                "You cannot register as an admin."
            )
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating user profiles."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "company_name",
            "bio",
            "phone",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "role", "date_joined"]


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user info used inside other serializers."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "company_name"]
        read_only_fields = fields
