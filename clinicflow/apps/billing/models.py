from django.db import models
from django.conf import settings


class Service(models.Model):
    clinic = models.ForeignKey("tenants.Clinic", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.clinic.name}"


class Invoice(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    clinic = models.ForeignKey("tenants.Clinic", on_delete=models.CASCADE)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.service_name} - {self.invoice.id}"