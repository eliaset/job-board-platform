"""
Tests for the jobs app — categories and job postings.
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import JobCategory, JobPosting

User = get_user_model()


class JobCategoryTests(TestCase):
    """Test job category CRUD endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/categories/"
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
            role="admin",
        )
        self.employer = User.objects.create_user(
            email="emp@example.com",
            password="emppass123",
            first_name="Emp",
            last_name="User",
            role="employer",
        )

    def test_list_categories_public(self):
        JobCategory.objects.create(name="Engineering")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            self.url, {"name": "Marketing", "description": "Marketing jobs"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_employer_forbidden(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(
            self.url, {"name": "Sales"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_duplicate_category(self):
        JobCategory.objects.create(name="Tech")
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            self.url, {"name": "Tech"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JobPostingTests(TestCase):
    """Test job posting CRUD and filtering."""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/jobs/"
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

    def test_list_jobs_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_job_as_employer(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(
            self.url,
            {
                "title": "Senior Python Developer",
                "description": "Looking for a Python dev.",
                "category": self.category.id,
                "location": "Addis Ababa",
                "job_type": "full_time",
                "salary_min": "50000.00",
                "salary_max": "80000.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Senior Python Developer")

    def test_create_job_as_seeker_forbidden(self):
        self.client.force_authenticate(user=self.seeker)
        response = self.client.post(
            self.url,
            {
                "title": "Test Job",
                "description": "Test",
                "location": "Addis Ababa",
                "job_type": "full_time",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_category(self):
        JobPosting.objects.create(
            title="Dev Job",
            description="Test",
            company=self.employer,
            category=self.category,
            location="Addis Ababa",
        )
        response = self.client.get(f"{self.url}?category={self.category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_filter_by_location(self):
        JobPosting.objects.create(
            title="Remote Dev",
            description="Test",
            company=self.employer,
            category=self.category,
            location="Remote",
        )
        response = self.client.get(f"{self.url}?location=Remote")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_salary_validation(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(
            self.url,
            {
                "title": "Invalid Salary Job",
                "description": "Test",
                "location": "Addis Ababa",
                "job_type": "full_time",
                "salary_min": "90000.00",
                "salary_max": "50000.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
