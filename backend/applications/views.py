"""
Views for Job Applications.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsJobSeeker, IsEmployerOrAdmin
from .models import JobApplication
from .serializers import (
    JobApplicationCreateSerializer,
    JobApplicationListSerializer,
    JobApplicationStatusSerializer,
)


@extend_schema(tags=["Applications"])
class ApplyToJobView(generics.CreateAPIView):
    """Submit a job application (job seekers only)."""

    serializer_class = JobApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobSeeker]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response(
            {
                "message": "Application submitted successfully.",
                "application": {
                    "id": application.id,
                    "job": application.job.title,
                    "status": application.status,
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Applications"])
class MyApplicationsView(generics.ListAPIView):
    """List all applications for the authenticated job seeker."""

    serializer_class = JobApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return (
            JobApplication.objects.filter(applicant=self.request.user)
            .select_related("job__company", "job__category", "applicant")
        )


@extend_schema(tags=["Applications"])
class JobApplicationsView(generics.ListAPIView):
    """
    List all applications for a specific job posting.
    Only the employer who posted the job (or an admin) can view these.
    """

    serializer_class = JobApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrAdmin]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        qs = (
            JobApplication.objects.filter(job_id=job_id)
            .select_related("job__company", "job__category", "applicant")
        )
        # Employers can only see applications for their own job postings
        if self.request.user.role == "employer":
            qs = qs.filter(job__company=self.request.user)
        return qs


@extend_schema(tags=["Applications"])
class UpdateApplicationStatusView(generics.UpdateAPIView):
    """
    Update the status of a job application.
    Only the employer who owns the job (or an admin) can update it.
    """

    serializer_class = JobApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrAdmin]

    def get_queryset(self):
        qs = JobApplication.objects.select_related("job__company")
        if self.request.user.role == "employer":
            qs = qs.filter(job__company=self.request.user)
        return qs
