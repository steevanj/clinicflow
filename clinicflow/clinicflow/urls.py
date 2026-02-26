"""
ClinicFlow Main URL Configuration
Production-ready central routing.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ==========================
    # Admin
    # ==========================
    path("admin/", admin.site.urls),

    # ==========================
    # Authentication
    # ==========================
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/", include("apps.accounts.urls")),  # only auth-related custom routes

    # ==========================
    # Core App Routes
    # ==========================
    path("api/accounts/", include("apps.accounts.urls")),  # user management
    path("api/tenants/", include("apps.tenants.urls")),
    path("api/subscriptions/", include("apps.subscriptions.urls")),
    path("api/patients/", include("apps.patients.urls")),
    path("api/doctors/", include("apps.doctors.urls")),
    path("api/staff/", include("apps.staff.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    path("api/reports/", include("apps.reports.urls")),
]