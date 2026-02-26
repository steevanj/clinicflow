from django.db import models
from django.conf import settings


class Patient(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    clinic = models.ForeignKey(
        "tenants.Clinic",
        on_delete=models.CASCADE,
        related_name="patients"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    gender = models.CharField(max_length=20)
    dob = models.DateField()

    address = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["clinic"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"