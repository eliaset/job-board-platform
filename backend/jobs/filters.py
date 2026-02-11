"""
Django-filter filter sets for job postings.
"""

import django_filters
from django.db import models
from .models import JobPosting


class JobPostingFilter(django_filters.FilterSet):
    """Filter set for job postings with range and keyword support."""

    category = django_filters.NumberFilter(field_name="category__id")
    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    job_type = django_filters.CharFilter(field_name="job_type")
    location = django_filters.CharFilter(
        field_name="location", lookup_expr="icontains"
    )
    salary_min = django_filters.NumberFilter(
        field_name="salary_min", lookup_expr="gte"
    )
    salary_max = django_filters.NumberFilter(
        field_name="salary_max", lookup_expr="lte"
    )
    is_active = django_filters.BooleanFilter(field_name="is_active")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = JobPosting
        fields = [
            "category",
            "category_name",
            "job_type",
            "location",
            "salary_min",
            "salary_max",
            "is_active",
        ]

    def filter_search(self, queryset, name, value):
        """Search in title, description, and location."""
        return queryset.filter(
            models.Q(title__icontains=value)
            | models.Q(description__icontains=value)
            | models.Q(location__icontains=value)
        )
