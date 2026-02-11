"""
Views for user registration, login (JWT), and profile management.
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, UserProfileSerializer

User = get_user_model()


@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    """Register a new user (job_seeker or employer)."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Auth"])
class LoginView(TokenObtainPairView):
    """Obtain JWT access and refresh tokens."""

    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["Auth"])
class TokenRefreshView(TokenRefreshView):
    """Refresh an expired access token."""

    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["Auth"])
class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
