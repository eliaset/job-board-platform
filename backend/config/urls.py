"""
Main URL configuration for Job Board Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


def api_root(request):
    """API root — welcome message with available endpoints."""
    return JsonResponse({
        "message": "Welcome to the Job Board Platform API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/api/docs/",
            "redoc": "/api/redoc/",
            "auth": "/api/auth/",
            "categories": "/api/categories/",
            "jobs": "/api/jobs/",
            "applications": "/api/applications/",
        }
    })


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    # App URLs
    path("api/auth/", include("accounts.urls")),
    path("api/categories/", include("jobs.urls_categories")),
    path("api/jobs/", include("jobs.urls_jobs")),
    path("api/applications/", include("applications.urls")),
    # OpenAPI / Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
