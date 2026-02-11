"""
Custom permissions for role-based access control.
"""

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Allow access only to users with the 'admin' role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsEmployer(BasePermission):
    """Allow access only to employers."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "employer"
        )


class IsJobSeeker(BasePermission):
    """Allow access only to job seekers."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "job_seeker"
        )


class IsEmployerOrAdmin(BasePermission):
    """Allow access to employers or admins."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("employer", "admin")
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission: only the owner of the object or an admin
    can modify it.  Requires the object to have a `company` or `user`
    attribute pointing to the owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        # Try common owner field names
        owner = getattr(obj, "company", None) or getattr(obj, "user", None)
        return owner == request.user
