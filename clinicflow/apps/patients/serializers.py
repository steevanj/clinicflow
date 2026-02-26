from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = (
            "id",
            "clinic",
            "created_at",
            "updated_at",
            "is_deleted",
        )

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["clinic"] = request.user.clinic
        return super().create(validated_data)