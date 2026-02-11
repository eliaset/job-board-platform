"""
Admin configuration for jobs app.
"""

from django.contrib import admin
from .models import JobCategory, JobPosting


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "company",
        "category",
        "location",
        "job_type",
        "is_active",
        "created_at",
    ]
    list_filter = ["job_type", "is_active", "category"]
    search_fields = ["title", "description", "location"]
    ordering = ["-created_at"]
