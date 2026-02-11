"""
Admin configuration for applications app.
"""

from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["applicant", "job", "status", "applied_at"]
    list_filter = ["status"]
    search_fields = ["applicant__email", "job__title"]
    ordering = ["-applied_at"]
