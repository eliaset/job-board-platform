"""
URL patterns for job categories.
"""

from django.urls import path
from .views import JobCategoryListCreateView, JobCategoryDetailView

urlpatterns = [
    path("", JobCategoryListCreateView.as_view(), name="category-list-create"),
    path("<int:pk>/", JobCategoryDetailView.as_view(), name="category-detail"),
]
