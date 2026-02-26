# staff/permissions.py

from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Only MANAGER role can manage staff
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "MANAGER"
        )