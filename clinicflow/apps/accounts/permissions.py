from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "SUPER_ADMIN"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MANAGER"