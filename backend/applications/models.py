"""
Model for Job Applications.
"""

from django.conf import settings
from django.db import models


class JobApplication(models.Model):
    """An application submitted by a job seeker for a job posting."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    job = models.ForeignKey(
        "jobs.JobPosting",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
        limit_choices_to={"role": "job_seeker"},
    )
    cover_letter = models.TextField(
        blank=True,
        default="",
        help_text="Optional cover letter for the application.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        # Ensure a user can apply to a job only once
        constraints = [
            models.UniqueConstraint(
                fields=["job", "applicant"],
                name="unique_application_per_job",
            )
        ]

    def __str__(self):
        return f"{self.applicant.email} → {self.job.title} ({self.status})"
