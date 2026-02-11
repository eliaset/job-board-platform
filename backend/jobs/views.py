"""
Views for Job Categories and Job Postings.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminUser, IsEmployerOrAdmin, IsOwnerOrAdmin
from .models import JobCategory, JobPosting
from .serializers import (
    JobCategorySerializer,
    JobPostingListSerializer,
    JobPostingDetailSerializer,
)
from .filters import JobPostingFilter


# ==========================================================================
# Job Category Views
# ==========================================================================

@extend_schema(tags=["Categories"])
class JobCategoryListCreateView(generics.ListCreateAPIView):
    """
    GET  – List all job categories (public).
    POST – Create a new category (admin only).
    """

    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]


@extend_schema(tags=["Categories"])
class JobCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    – Category detail (public).
    PUT    – Update category (admin only).
    DELETE – Delete category (admin only).
    """

    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]


# ==========================================================================
# Job Posting Views
# ==========================================================================

@extend_schema(tags=["Jobs"])
class JobPostingListCreateView(generics.ListCreateAPIView):
    """
    GET  – List jobs with filtering, sorting, and pagination (public).
    POST – Create a job posting (employer or admin only).
    """

    filterset_class = JobPostingFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["created_at", "salary_min", "salary_max", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return JobPosting.objects.select_related("company", "category").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JobPostingDetailSerializer
        return JobPostingListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsEmployerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)


@extend_schema(tags=["Jobs"])
class JobPostingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    – Job detail (public).
    PUT    – Update job (owner or admin).
    DELETE – Delete job (owner or admin).
    """

    serializer_class = JobPostingDetailSerializer

    def get_queryset(self):
        return JobPosting.objects.select_related("company", "category").all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.AllowAny()]
