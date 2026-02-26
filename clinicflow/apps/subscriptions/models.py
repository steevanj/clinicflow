from django.db import models
from apps.tenants.models import Clinic


class Plan(models.Model):
    BASIC = "Basic"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"

    PLAN_CHOICES = [
        (BASIC, "Basic"),
        (PRO, "Pro"),
        (ENTERPRISE, "Enterprise"),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    doctor_limit = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    clinic = models.ForeignKey(
    "tenants.Clinic",
    on_delete=models.CASCADE,
    related_name="subscriptions"
)
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.plan.name}"