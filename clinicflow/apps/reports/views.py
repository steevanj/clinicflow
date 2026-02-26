# reports/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.dateparse import parse_date

from .services import ReportService
from .exporters import CSVExporter, PDFExporter


class BaseReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_dates(self, request):
        start_date = parse_date(request.query_params.get("start_date"))
        end_date = parse_date(request.query_params.get("end_date"))
        return start_date, end_date

    def get_export_format(self, request):
        return request.query_params.get("format")


class AppointmentReportView(BaseReportView):

    def get(self, request):
        clinic = request.user.clinic
        start_date, end_date = self.get_dates(request)

        report = ReportService.appointment_report(clinic, start_date, end_date)

        format_type = self.get_export_format(request)

        if format_type == "csv":
            headers = ["Doctor ID", "First Name", "Last Name", "Total Appointments"]
            data = [
                [
                    r["doctor__id"],
                    r["doctor__first_name"],
                    r["doctor__last_name"],
                    r["total_appointments"],
                ]
                for r in report
            ]
            return CSVExporter.export("appointment_report", headers, data)

        if format_type == "pdf":
            headers = ["Doctor ID", "First Name", "Last Name", "Total Appointments"]
            data = [
                [
                    r["doctor__id"],
                    r["doctor__first_name"],
                    r["doctor__last_name"],
                    r["total_appointments"],
                ]
                for r in report
            ]
            return PDFExporter.export("appointment_report", headers, data)

        return Response(report)


class RevenueReportView(BaseReportView):

    def get(self, request):
        clinic = request.user.clinic
        start_date, end_date = self.get_dates(request)

        report = ReportService.revenue_report(clinic, start_date, end_date)

        format_type = self.get_export_format(request)

        if format_type == "csv":
            headers = ["Total Revenue", "Total Invoices"]
            data = [[report["total_revenue"], report["total_invoices"]]]
            return CSVExporter.export("revenue_report", headers, data)

        if format_type == "pdf":
            headers = ["Total Revenue", "Total Invoices"]
            data = [[report["total_revenue"], report["total_invoices"]]]
            return PDFExporter.export("revenue_report", headers, data)

        return Response(report)


class DoctorPerformanceReportView(BaseReportView):

    def get(self, request):
        clinic = request.user.clinic
        start_date, end_date = self.get_dates(request)

        report = ReportService.doctor_performance_report(clinic, start_date, end_date)

        format_type = self.get_export_format(request)

        if format_type == "csv":
            headers = ["Doctor ID", "First Name", "Last Name", "Completed Appointments"]
            data = [
                [
                    r["doctor__id"],
                    r["doctor__first_name"],
                    r["doctor__last_name"],
                    r["completed_appointments"],
                ]
                for r in report
            ]
            return CSVExporter.export("doctor_performance", headers, data)

        if format_type == "pdf":
            headers = ["Doctor ID", "First Name", "Last Name", "Completed Appointments"]
            data = [
                [
                    r["doctor__id"],
                    r["doctor__first_name"],
                    r["doctor__last_name"],
                    r["completed_appointments"],
                ]
                for r in report
            ]
            return PDFExporter.export("doctor_performance", headers, data)

        return Response(report)