# staff/models.py

from django.db import models
from django.conf import settings


class StaffProfile(models.Model):
    ROLE_CHOICES = (
        ("RECEPTIONIST", "Receptionist"),
        ("NURSE", "Nurse"),
        ("ADMIN", "Admin"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    clinic = models.ForeignKey(
        "tenants.Clinic",
        on_delete=models.CASCADE,
        related_name="staff_members"
    )

    designation = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.designation}"