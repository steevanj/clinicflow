from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    clinic = models.ForeignKey(
        "tenants.Clinic",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        "doctors.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "doctor",
            "appointment_date",
            "appointment_time",
        )
        ordering = ["-appointment_date", "-appointment_time"]

    def clean(self):
        # Prevent booking in the past
        appointment_datetime = timezone.make_aware(
            datetime.combine(self.appointment_date, self.appointment_time),
            timezone.get_current_timezone()
        )

        if appointment_datetime < timezone.now():
            raise ValidationError("Cannot book appointment in the past.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"
