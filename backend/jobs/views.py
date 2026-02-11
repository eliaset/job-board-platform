"""
Views for Job Categories, Job Postings, Saved Jobs, and Employer Stats.
"""

from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminUser, IsEmployerOrAdmin, IsOwnerOrAdmin
from .models import JobCategory, JobPosting, SavedJob
from .serializers import (
    JobCategorySerializer,
    JobPostingListSerializer,
    JobPostingDetailSerializer,
    SavedJobSerializer,
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


# ==========================================================================
# Saved / Bookmarked Jobs
# ==========================================================================

@extend_schema(tags=["Saved Jobs"])
class SavedJobListView(generics.ListAPIView):
    """List all jobs saved by the authenticated user."""

    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related(
            "job__company", "job__category"
        )


@extend_schema(tags=["Saved Jobs"])
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_save_job(request, job_id):
    """Save or unsave a job (toggle). Returns the new saved state."""
    try:
        job = JobPosting.objects.get(pk=job_id)
    except JobPosting.DoesNotExist:
        return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved.delete()
        return Response({"saved": False, "message": "Job unsaved."})
    return Response({"saved": True, "message": "Job saved."}, status=status.HTTP_201_CREATED)


# ==========================================================================
# Employer Statistics / Analytics
# ==========================================================================

@extend_schema(tags=["Jobs"])
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def employer_stats(request):
    """Dashboard statistics for the authenticated employer."""
    user = request.user
    jobs = JobPosting.objects.filter(company=user)
    jobs_with_counts = jobs.annotate(app_count=Count("applications"))

    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    total_applications = sum(j.app_count for j in jobs_with_counts)

    top_jobs = jobs_with_counts.order_by("-app_count")[:5].values(
        "id", "title", "app_count", "is_active", "created_at"
    )

    return Response({
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_applications": total_applications,
        "top_jobs": list(top_jobs),
    })
