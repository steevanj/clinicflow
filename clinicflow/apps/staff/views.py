# staff/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import StaffProfile
from .serializers import (
    StaffSerializer,
    StaffCreateSerializer,
)
from .permissions import IsManager


class StaffListCreateAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        staff = StaffProfile.objects.filter(
            clinic=request.user.clinic
        )

        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            staff = serializer.save()
            return Response(
                StaffSerializer(staff).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StaffDetailAPIView(APIView):
    permission_classes = [IsManager]

    def get_object(self, request, pk):
        return get_object_or_404(
            StaffProfile,
            pk=pk,
            clinic=request.user.clinic
        )

    def get(self, request, pk):
        staff = self.get_object(request, pk)
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    def put(self, request, pk):
        staff = self.get_object(request, pk)
        serializer = StaffSerializer(
            staff,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        staff = self.get_object(request, pk)

        staff.user.delete()  # also deletes profile
        return Response(status=status.HTTP_204_NO_CONTENT)