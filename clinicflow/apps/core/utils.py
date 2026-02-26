import uuid
from django.utils.text import slugify


def generate_uuid():
    return uuid.uuid4()


def generate_unique_slug(instance, field_name, new_slug=None):
    slug = new_slug if new_slug else slugify(getattr(instance, field_name))
    Klass = instance.__class__

    if Klass.objects.filter(slug=slug).exists():
        return generate_unique_slug(instance, field_name, f"{slug}-{uuid.uuid4().hex[:6]}")

    return slug


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def model_to_dict(instance, fields=None):
    data = {}
    for field in fields or [f.name for f in instance._meta.fields]:
        data[field] = getattr(instance, field)
    return data