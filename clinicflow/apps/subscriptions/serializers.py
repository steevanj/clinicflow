# subscriptions/serializers.py

from rest_framework import serializers
from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "doctor_limit", "price", "features"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = ["id", "plan", "started_at", "is_active"]