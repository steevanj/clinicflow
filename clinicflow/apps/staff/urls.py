# staff/urls.py

from django.urls import path
from .views import (
    StaffListCreateAPIView,
    StaffDetailAPIView,
)

urlpatterns = [
    path("", StaffListCreateAPIView.as_view()),
    path("<int:pk>/", StaffDetailAPIView.as_view()),
]