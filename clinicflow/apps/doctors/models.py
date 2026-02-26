from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic
from datetime import datetime
from apps.appointments.models import Appointment


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    specialization = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # Example structure:
    # {
    #   "monday": {"start": "09:00", "end": "17:00"},
    #   "tuesday": {"start": "09:00", "end": "17:00"},
    #   ...
    # }
    availability_schedule = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "doctor_profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.specialization}"

    def is_available_on(self, date, time):
        """
        Check if doctor is available on given date and time.
        Uses availability_schedule JSON field and also checks for conflicts.
        """
        weekday = date.strftime("%A").lower()
        schedule = self.availability_schedule.get(weekday)

        if not schedule:
            return False

        start = datetime.strptime(schedule["start"], "%H:%M").time()
        end = datetime.strptime(schedule["end"], "%H:%M").time()

        within_hours = start <= time <= end

        # Also check if doctor already has an appointment at that time
        has_conflict = Appointment.objects.filter(
            doctor=self,
            appointment_date=date,
            appointment_time=time
        ).exists()

        return within_hours and not has_conflict
