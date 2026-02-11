"""
URL patterns for job applications.
"""

from django.urls import path
from .views import (
    ApplyToJobView,
    MyApplicationsView,
    JobApplicationsView,
    UpdateApplicationStatusView,
)

urlpatterns = [
    path("apply/", ApplyToJobView.as_view(), name="apply-to-job"),
    path("my/", MyApplicationsView.as_view(), name="my-applications"),
    path(
        "job/<int:job_id>/",
        JobApplicationsView.as_view(),
        name="job-applications",
    ),
    path(
        "<int:pk>/status/",
        UpdateApplicationStatusView.as_view(),
        name="update-application-status",
    ),
]
