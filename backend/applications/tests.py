"""
Tests for the applications app — apply, view, and manage applications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from jobs.models import JobCategory, JobPosting
from .models import JobApplication

User = get_user_model()


class JobApplicationTests(TestCase):
    """Test job application endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.employer = User.objects.create_user(
            email="emp@example.com",
            password="emppass123",
            first_name="Emp",
            last_name="User",
            role="employer",
            company_name="TechCorp",
        )
        self.seeker = User.objects.create_user(
            email="seeker@example.com",
            password="seekpass123",
            first_name="Seeker",
            last_name="User",
            role="job_seeker",
        )
        self.category = JobCategory.objects.create(name="Engineering")
        self.job = JobPosting.objects.create(
            title="Python Developer",
            description="Looking for a Python dev.",
            company=self.employer,
            category=self.category,
            location="Addis Ababa",
            job_type="full_time",
        )

    def test_apply_as_seeker(self):
        self.client.force_authenticate(user=self.seeker)
        response = self.client.post(
            "/api/applications/apply/",
            {"job": self.job.id, "cover_letter": "I am interested!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_apply_as_employer_forbidden(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(
            "/api/applications/apply/",
            {"job": self.job.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_duplicate_application(self):
        self.client.force_authenticate(user=self.seeker)
        self.client.post(
            "/api/applications/apply/",
            {"job": self.job.id},
            format="json",
        )
        response = self.client.post(
            "/api/applications/apply/",
            {"job": self.job.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_my_applications(self):
        self.client.force_authenticate(user=self.seeker)
        JobApplication.objects.create(
            job=self.job, applicant=self.seeker, cover_letter="Test"
        )
        response = self.client.get("/api/applications/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_employer_view_applications(self):
        JobApplication.objects.create(
            job=self.job, applicant=self.seeker, cover_letter="Test"
        )
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(f"/api/applications/job/{self.job.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_application_status(self):
        app = JobApplication.objects.create(
            job=self.job, applicant=self.seeker, cover_letter="Test"
        )
        self.client.force_authenticate(user=self.employer)
        response = self.client.patch(
            f"/api/applications/{app.id}/status/",
            {"status": "reviewed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "reviewed")

    def test_apply_to_inactive_job(self):
        self.job.is_active = False
        self.job.save()
        self.client.force_authenticate(user=self.seeker)
        response = self.client.post(
            "/api/applications/apply/",
            {"job": self.job.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
