# subscriptions/services.py

from django.core.exceptions import ValidationError
from .models import Subscription, Plan


def upgrade_subscription(clinic, plan_id):
    try:
        new_plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        raise ValidationError("Invalid plan selected")

    subscription, created = Subscription.objects.get_or_create(
        clinic=clinic,
        defaults={"plan": new_plan}
    )

    if not created:
        subscription.plan = new_plan
        subscription.save()

    return subscription