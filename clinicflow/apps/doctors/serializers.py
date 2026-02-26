from rest_framework import serializers
from apps.accounts.models import User
from .models import DoctorProfile


class DoctorProfileSerializer(serializers.ModelSerializer):
    # Map to User fields for output
    name = serializers.CharField(source="user.full_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "specialization",
            "experience_years",
            "consultation_fee",
            "availability_schedule",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_availability_schedule(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid schedule format.")
        for day, slots in value.items():
            if not isinstance(slots, list):
                raise serializers.ValidationError(f"Slots must be list for {day}")
        return value

    def create(self, validated_data):
        # Extract raw fields from request data
        request_data = self.context["request"].data
        name = request_data.get("name")
        phone = request_data.get("phone")
        email = request_data.get("email")

        clinic = getattr(self.context["request"].user, "clinic", None)
        if clinic is None:
            raise serializers.ValidationError({"clinic": "Clinic is required."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # Create user for doctor
        user = User.objects.create_user(
            email=email,
            role="DOCTOR",
            clinic=clinic
        )
        user.full_name = name
        user.phone = phone
        user.save()

        doctor = DoctorProfile.objects.create(
            user=user,
            clinic=clinic,
            **validated_data
        )
        return doctor
