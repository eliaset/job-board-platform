"""
Models for Job Categories and Job Postings.
"""

from django.conf import settings
from django.db import models


class JobCategory(models.Model):
    """Industry or domain category for job postings."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """A job listing created by an employer."""

    class JobType(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        PART_TIME = "part_time", "Part Time"
        CONTRACT = "contract", "Contract"
        REMOTE = "remote", "Remote"
        INTERNSHIP = "internship", "Internship"

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_postings",
        limit_choices_to={"role": "employer"},
    )
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_postings",
    )
    location = models.CharField(max_length=255, db_index=True)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME,
        db_index=True,
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    requirements = models.TextField(
        blank=True,
        default="",
        help_text="Job requirements and qualifications.",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["job_type", "is_active"]),
            models.Index(fields=["location", "is_active"]),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.company_name or self.company.email}"
