# tenants/serializers.py

from rest_framework import serializers
from .models import Clinic


class ClinicSerializer(serializers.ModelSerializer):

    subscription = serializers.StringRelatedField()

    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "slug",
            "phone",
            "email",
            "address",
            "subscription",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ClinicUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clinic
        fields = [
            "name",
            "phone",
            "email",
            "address",
        ]