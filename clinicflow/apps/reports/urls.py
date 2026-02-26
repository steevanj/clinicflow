# reports/urls.py

from django.urls import path
from .views import (
    AppointmentReportView,
    RevenueReportView,
    DoctorPerformanceReportView,
)

urlpatterns = [
    path("appointments/", AppointmentReportView.as_view()),
    path("revenue/", RevenueReportView.as_view()),
    path("doctor-performance/", DoctorPerformanceReportView.as_view()),
]