from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        clinic = user.clinic

        queryset = Appointment.objects.filter(clinic=clinic)

        # Doctor sees only their appointments
        if user.role == "DOCTOR":
            queryset = queryset.filter(doctor__user=user)

        # Filtering
        doctor = request.query_params.get("doctor")
        date = request.query_params.get("date")
        status_param = request.query_params.get("status")

        if doctor:
            queryset = queryset.filter(doctor_id=doctor)

        if date:
            queryset = queryset.filter(appointment_date=date)

        if status_param:
            queryset = queryset.filter(status=status_param)

        # Pagination
        page_number = request.query_params.get("page", 1)
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(page_number)

        serializer = AppointmentSerializer(page_obj, many=True)

        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "results": serializer.data
        })

    def post(self, request):
        user = request.user

        # Only Super Admin, Manager, or Receptionist can create
        if user.role not in ["SUPER_ADMIN", "MANAGER", "RECEPTIONIST"]:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(clinic=user.clinic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        clinic = user.clinic
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            clinic=clinic
        )

        # Doctors can only access their own appointments
        if user.role == "DOCTOR" and appointment.doctor.user != user:
            return None

        return appointment

    def get(self, request, pk):
        appointment = self.get_object(request.user, pk)

        if not appointment:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        appointment = self.get_object(user, pk)

        if not appointment:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=False
        )

        if serializer.is_valid():
            serializer.save(clinic=user.clinic)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        appointment = self.get_object(user, pk)

        if not appointment:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
