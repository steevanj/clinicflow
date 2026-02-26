# staff/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StaffProfile

User = get_user_model()


class StaffCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    designation = serializers.ChoiceField(
        choices=StaffProfile.ROLE_CHOICES
    )

    def create(self, validated_data):
        request = self.context["request"]
        clinic = request.user.clinic

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["designation"],
            clinic=clinic,
        )

        staff = StaffProfile.objects.create(
            user=user,
            clinic=clinic,
            designation=validated_data["designation"],
        )

        return staff


class StaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = StaffProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "designation",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        instance.designation = validated_data.get(
            "designation",
            instance.designation
        )

        instance.user.first_name = user_data.get(
            "first_name",
            instance.user.first_name
        )

        instance.user.last_name = user_data.get(
            "last_name",
            instance.user.last_name
        )

        instance.user.email = user_data.get(
            "email",
            instance.user.email
        )

        instance.user.save()
        instance.save()

        return instance