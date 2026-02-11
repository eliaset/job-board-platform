"""
URL patterns for job postings, saved jobs, and employer stats.
"""

from django.urls import path
from .views import (
    JobPostingListCreateView,
    JobPostingDetailView,
    SavedJobListView,
    toggle_save_job,
    employer_stats,
)

urlpatterns = [
    path("", JobPostingListCreateView.as_view(), name="job-list-create"),
    path("saved/", SavedJobListView.as_view(), name="saved-jobs"),
    path("stats/", employer_stats, name="employer-stats"),
    path("<int:pk>/", JobPostingDetailView.as_view(), name="job-detail"),
    path("<int:job_id>/save/", toggle_save_job, name="toggle-save-job"),
]
