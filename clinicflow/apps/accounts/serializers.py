from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from .models import User
from apps.tenants.models import Clinic
from apps.subscriptions.models import Plan


class RegisterSerializer(serializers.Serializer):
    clinic_name = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True)
    plan = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default="MANAGER")  # <-- NEW

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # Lookup plan by name
        plan_name = validated_data.get("plan", Plan.BASIC)
        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            raise serializers.ValidationError({"plan": "Invalid subscription plan"})

        # Create clinic with subscription
        clinic = Clinic.objects.create(
            name=validated_data["clinic_name"],
            email=validated_data["email"],
            phone=validated_data.get("phone", ""),
            address=validated_data.get("address", ""),
            subscription=plan
        )

        # Create user with requested role
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],   # <-- use provided role
            clinic=clinic,
            is_staff=True,
            is_verified=True,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account disabled")
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            uid = smart_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(id=uid)
        except Exception:
            raise serializers.ValidationError("Invalid reset link")

        if not PasswordResetTokenGenerator().check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        validate_password(data["password"])
        user.set_password(data["password"])
        user.save()
        return user
