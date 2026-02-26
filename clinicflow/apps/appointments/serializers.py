from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("clinic", "created_at", "updated_at")

    def validate(self, data):
        doctor = data.get("doctor")
        date = data.get("appointment_date")
        time = data.get("appointment_time")

        # Prevent double booking (extra safety)
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            appointment_time=time
        ).exists():
            raise serializers.ValidationError(
                "Doctor already has an appointment at this time."
            )

        # Validate doctor availability (example)
        if not doctor.is_available_on(date, time):
            raise serializers.ValidationError(
                "Doctor not available at selected time."
            )

        return data