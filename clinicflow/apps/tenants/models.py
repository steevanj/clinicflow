# tenants/models.py

import uuid
from django.db import models
from django.utils.text import slugify


class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    subscription = models.ForeignKey(
        "subscriptions.Plan",
        on_delete=models.PROTECT,
        related_name="clinics"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clinics"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name