# doctors/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import DoctorProfile
from .serializers import DoctorProfileSerializer
from .permissions import IsManager
from .services import check_doctor_limit


class DoctorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        doctors = DoctorProfile.objects.filter(
            clinic=request.user.clinic
        )
        serializer = DoctorProfileSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        clinic = request.user.clinic

        # 🔥 Subscription limit enforcement
        check_doctor_limit(clinic)

        serializer = DoctorProfileSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get_object(self, request, pk):
        return get_object_or_404(
            DoctorProfile,
            pk=pk,
            clinic=request.user.clinic
        )

    def get(self, request, pk):
        doctor = self.get_object(request, pk)
        serializer = DoctorProfileSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self.get_object(request, pk)
        serializer = DoctorProfileSerializer(
            doctor,
            data=request.data,
            partial=True,  # allows partial updates
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(request, pk)
        doctor.user.delete()  # deletes profile via cascade
        return Response(
            {"message": "Doctor removed successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
