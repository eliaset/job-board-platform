"""
Custom User model with role-based access control.

Roles:
    - admin: Can manage everything (categories, jobs, users).
    - employer: Can create/manage job postings and review applications.
    - job_seeker: Can browse jobs and submit applications.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager that uses email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", User.Role.JOB_SEEKER)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model using email as the login credential."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        EMPLOYER = "employer", "Employer"
        JOB_SEEKER = "job_seeker", "Job Seeker"

    # Remove default username field; use email instead
    username = None
    email = models.EmailField("email address", unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOB_SEEKER,
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Company name (relevant for employers).",
    )
    bio = models.TextField(
        blank=True,
        default="",
        help_text="Short bio or description.",
    )
    phone = models.CharField(max_length=20, blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    @property
    def is_job_seeker(self):
        return self.role == self.Role.JOB_SEEKER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN
