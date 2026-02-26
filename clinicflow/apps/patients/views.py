from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .serializers import PatientSerializer
from .permissions import IsPatientAllowed


class PatientPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# 🔹 LIST + CREATE
class PatientListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPatientAllowed]

    def get(self, request):
        clinic = request.user.clinic

        queryset = Patient.objects.filter(
            clinic=clinic,
            is_deleted=False
        )

        # 🔍 Search
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )

        # 🔎 Filter by status
        status_param = request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)

        paginator = PatientPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = PatientSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 RETRIEVE + UPDATE + DELETE
class PatientDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPatientAllowed]

    def get_object(self, pk, user):
        return Patient.objects.filter(
            pk=pk,
            clinic=user.clinic,
            is_deleted=False
        ).first()

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PatientSerializer(
            patient,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        patient.is_deleted = True
        patient.save()

        return Response(
            {"detail": "Patient soft deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )