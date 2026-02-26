# reports/services.py

from django.db.models import Count, Sum, F
from django.utils import timezone
from apps.appointments.models import Appointment
from apps.billing.models import Invoice
from apps.accounts.models import User


class ReportService:

    @staticmethod
    def appointment_report(clinic, start_date=None, end_date=None):
        qs = Appointment.objects.filter(clinic=clinic)

        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        return qs.values(
            "doctor__id",
            "doctor__first_name",
            "doctor__last_name",
        ).annotate(
            total_appointments=Count("id")
        )

    @staticmethod
    def revenue_report(clinic, start_date=None, end_date=None):
        qs = Invoice.objects.filter(clinic=clinic, status="paid")

        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)

        return qs.aggregate(
            total_revenue=Sum("amount"),
            total_invoices=Count("id")
        )

    @staticmethod
    def doctor_performance_report(clinic, start_date=None, end_date=None):
        qs = Appointment.objects.filter(clinic=clinic, status="completed")

        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        return qs.values(
            "doctor__id",
            "doctor__first_name",
            "doctor__last_name"
        ).annotate(
            completed_appointments=Count("id")
        ).order_by("-completed_appointments")