from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
from apps.billing.models import Invoice, InvoiceItem
from apps.doctors.models import DoctorProfile


class AnalyticsService:

    @staticmethod
    def apply_date_filter(queryset, start_date, end_date):
        if start_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(end_date))
        return queryset

    @staticmethod
    def monthly_revenue(clinic, start_date=None, end_date=None):
        qs = Invoice.objects.filter(clinic=clinic, status="PAID")

        qs = AnalyticsService.apply_date_filter(qs, start_date, end_date)

        data = (
            qs.annotate(month=TruncMonth("created_at"))
              .values("month")
              .annotate(total_revenue=Sum("total_amount"))
              .order_by("month")
        )

        return [
            {
                "month": item["month"].strftime("%Y-%m"),
                "revenue": item["total_revenue"] or 0
            }
            for item in data
        ]

    @staticmethod
    def revenue_by_doctor(clinic, start_date=None, end_date=None):
        qs = Invoice.objects.filter(clinic=clinic, status="PAID")

        qs = AnalyticsService.apply_date_filter(qs, start_date, end_date)

        data = (
            qs.values("doctor__id", "doctor__user__first_name", "doctor__user__last_name")
              .annotate(total_revenue=Sum("total_amount"))
              .order_by("-total_revenue")
        )

        return [
            {
                "doctor_id": item["doctor__id"],
                "doctor_name": f"{item['doctor__user__first_name']} {item['doctor__user__last_name']}",
                "revenue": item["total_revenue"] or 0
            }
            for item in data
        ]

    @staticmethod
    def revenue_by_service(clinic, start_date=None, end_date=None):
        qs = InvoiceItem.objects.filter(invoice__clinic=clinic, invoice__status="PAID")

        if start_date:
            qs = qs.filter(invoice__created_at__date__gte=parse_date(start_date))
        if end_date:
            qs = qs.filter(invoice__created_at__date__lte=parse_date(end_date))

        data = (
            qs.values("service_name")
              .annotate(total_revenue=Sum(F("quantity") * F("price")))
              .order_by("-total_revenue")
        )

        return [
            {
                "service_name": item["service_name"],
                "revenue": item["total_revenue"] or 0
            }
            for item in data
        ]