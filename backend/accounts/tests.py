"""
Tests for the accounts app — registration, login, and profile management.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test user registration endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"

    def test_register_job_seeker(self):
        data = {
            "email": "seeker@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "job_seeker",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["role"], "job_seeker")

    def test_register_employer(self):
        data = {
            "email": "employer@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "role": "employer",
            "company_name": "Tech Corp",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["role"], "employer")

    def test_register_admin_blocked(self):
        data = {
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "job_seeker",
            "password": "strongpass123",
            "password_confirm": "wrongpass",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email="dupe@example.com",
            password="pass1234",
            first_name="A",
            last_name="B",
        )
        data = {
            "email": "dupe@example.com",
            "first_name": "C",
            "last_name": "D",
            "role": "job_seeker",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    """Test JWT login endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"email": "user@example.com", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"email": "user@example.com", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTests(TestCase):
    """Test profile retrieval and update."""

    def setUp(self):
        self.client = APIClient()
        self.profile_url = "/api/auth/profile/"
        self.user = User.objects.create_user(
            email="profile@example.com",
            password="testpass123",
            first_name="Profile",
            last_name="User",
            role="job_seeker",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "profile@example.com")

    def test_update_profile(self):
        response = self.client.put(
            self.profile_url,
            {"first_name": "Updated", "last_name": "Name", "bio": "New bio"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
