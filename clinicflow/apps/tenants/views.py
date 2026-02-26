from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Clinic
from .serializers import ClinicSerializer, ClinicUpdateSerializer


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MANAGER"


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class ClinicMeView(APIView):
    """
    GET /api/clinics/me/
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        clinic = getattr(request.user, "clinic", None)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=400)

        serializer = ClinicSerializer(clinic)
        return Response(serializer.data)


class ClinicUpdateView(APIView):
    """
    PUT /api/clinics/update/
    """

    permission_classes = [permissions.IsAuthenticated, IsManager]

    def put(self, request):
        clinic = getattr(request.user, "clinic", None)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=400)

        serializer = ClinicUpdateSerializer(clinic, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Clinic updated successfully"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClinicListView(APIView):
    """
    Super Admin only
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        clinics = Clinic.objects.all()
        serializer = ClinicSerializer(clinics, many=True)
        return Response(serializer.data)
