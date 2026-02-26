# subscriptions/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer
from .permissions import IsManager
from .services import upgrade_subscription


class PlanListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.all().order_by("price")
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)


class CurrentSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinic = request.user.clinic

        try:
            subscription = Subscription.objects.get(clinic=clinic)
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)


class UpgradeSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        clinic = request.user.clinic
        plan_id = request.data.get("plan_id")

        if not plan_id:
            return Response(
                {"detail": "plan_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = upgrade_subscription(clinic, plan_id)

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)