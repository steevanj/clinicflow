from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("SUPER_ADMIN", "Super Admin"),
        ("MANAGER", "Manager"),
        ("DOCTOR", "Doctor"),
        ("RECEPTIONIST", "Receptionist"),
        ("STAFF", "Staff"),
    )

    id = models.BigAutoField(primary_key=True)

    clinic = models.ForeignKey(
        "tenants.Clinic",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email