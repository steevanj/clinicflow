from django.urls import path
from .views import (
    MonthlyRevenueAPIView,
    RevenueByDoctorAPIView,
    RevenueByServiceAPIView,
)

urlpatterns = [
    path("monthly-revenue/", MonthlyRevenueAPIView.as_view(), name="monthly-revenue"),
    path("revenue-by-doctor/", RevenueByDoctorAPIView.as_view(), name="revenue-by-doctor"),
    path("revenue-by-service/", RevenueByServiceAPIView.as_view(), name="revenue-by-service"),
]