from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import AnalyticsService


class MonthlyRevenueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinic = request.user.clinic

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        data = AnalyticsService.monthly_revenue(
            clinic=clinic,
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            "chart_type": "line",
            "data": data
        })


class RevenueByDoctorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinic = request.user.clinic

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        data = AnalyticsService.revenue_by_doctor(
            clinic=clinic,
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            "chart_type": "bar",
            "data": data
        })


class RevenueByServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinic = request.user.clinic

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        data = AnalyticsService.revenue_by_service(
            clinic=clinic,
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            "chart_type": "pie",
            "data": data
        })