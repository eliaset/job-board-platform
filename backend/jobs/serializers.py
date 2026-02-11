"""
Serializers for JobCategory and JobPosting.
"""

from rest_framework import serializers
from accounts.serializers import UserMinimalSerializer
from .models import JobCategory, JobPosting


class JobCategorySerializer(serializers.ModelSerializer):
    """Full serializer for job categories."""

    job_count = serializers.SerializerMethodField()

    class Meta:
        model = JobCategory
        fields = ["id", "name", "description", "job_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_job_count(self, obj):
        return obj.job_postings.filter(is_active=True).count()


class JobPostingListSerializer(serializers.ModelSerializer):
    """Serializer for listing jobs (lightweight)."""

    company = UserMinimalSerializer(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    job_type_display = serializers.CharField(source="get_job_type_display", read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "company",
            "category",
            "category_name",
            "location",
            "job_type",
            "job_type_display",
            "salary_min",
            "salary_max",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "company", "created_at"]


class JobPostingDetailSerializer(serializers.ModelSerializer):
    """Full serializer for job detail / create / update."""

    company = UserMinimalSerializer(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    job_type_display = serializers.CharField(source="get_job_type_display", read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "company",
            "category",
            "category_name",
            "location",
            "job_type",
            "job_type_display",
            "salary_min",
            "salary_max",
            "requirements",
            "is_active",
            "application_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "company", "created_at", "updated_at"]

    def get_application_count(self, obj):
        return obj.applications.count()

    def validate(self, data):
        salary_min = data.get("salary_min")
        salary_max = data.get("salary_max")
        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError(
                {"salary_max": "Maximum salary must be greater than minimum salary."}
            )
        return data
