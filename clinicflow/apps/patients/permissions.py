from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPatientAllowed(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        role = request.user.role  # assuming role field in custom user

        if request.method in SAFE_METHODS:
            return role in ["MANAGER", "RECEPTIONIST", "DOCTOR"]

        return role in ["MANAGER", "RECEPTIONIST"]