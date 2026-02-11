"""
Serializers for Job Applications.
"""

from rest_framework import serializers
from accounts.serializers import UserMinimalSerializer
from jobs.serializers import JobPostingListSerializer
from .models import JobApplication


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a job application."""

    class Meta:
        model = JobApplication
        fields = ["id", "job", "cover_letter", "status", "applied_at"]
        read_only_fields = ["id", "status", "applied_at"]

    def validate_job(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "This job posting is no longer active."
            )
        return value

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user:
            if request.user.role != "job_seeker":
                raise serializers.ValidationError(
                    "Only job seekers can apply for jobs."
                )
            # Check for duplicate application
            if JobApplication.objects.filter(
                job=data["job"], applicant=request.user
            ).exists():
                raise serializers.ValidationError(
                    "You have already applied for this job."
                )
        return data

    def create(self, validated_data):
        validated_data["applicant"] = self.context["request"].user
        return super().create(validated_data)


class JobApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for listing applications with related data."""

    applicant = UserMinimalSerializer(read_only=True)
    job = JobPostingListSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "applicant",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]
        read_only_fields = fields


class JobApplicationStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating application status."""

    class Meta:
        model = JobApplication
        fields = ["id", "status", "updated_at"]
        read_only_fields = ["id", "updated_at"]

    def validate_status(self, value):
        allowed = [s[0] for s in JobApplication.Status.choices]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed)}"
            )
        return value
