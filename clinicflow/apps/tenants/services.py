# tenants/services.py

from django.utils.text import slugify
from .models import Clinic


class ClinicService:

    @staticmethod
    def create_clinic(data):
        """
        Handles clinic creation logic.
        Can be extended with billing, onboarding logic etc.
        """

        slug = slugify(data["name"])

        if Clinic.objects.filter(slug=slug).exists():
            raise ValueError("Clinic with this name already exists")

        clinic = Clinic.objects.create(
            name=data["name"],
            slug=slug,
            phone=data["phone"],
            email=data["email"],
            address=data["address"],
            subscription=data["subscription"],
        )

        return clinic