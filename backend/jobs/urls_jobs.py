"""
URL patterns for job postings.
"""

from django.urls import path
from .views import JobPostingListCreateView, JobPostingDetailView

urlpatterns = [
    path("", JobPostingListCreateView.as_view(), name="job-list-create"),
    path("<int:pk>/", JobPostingDetailView.as_view(), name="job-detail"),
]
