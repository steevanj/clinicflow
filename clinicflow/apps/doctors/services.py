from rest_framework.exceptions import ValidationError
from .models import DoctorProfile


def check_doctor_limit(clinic):
    """
    Validate doctor count based on clinic subscription.
    """

    # clinic.subscription is a ForeignKey to Plan
    subscription_plan = clinic.subscription  
    max_doctors = subscription_plan.doctor_limit  # correct field

    current_count = DoctorProfile.objects.filter(clinic=clinic).count()

    if current_count >= max_doctors:
        raise ValidationError(
            f"Doctor limit exceeded. Plan allows only {max_doctors} doctors."
        )
