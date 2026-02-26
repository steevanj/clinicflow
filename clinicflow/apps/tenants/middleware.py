# tenants/middleware.py

from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Clinic


class ClinicMiddleware(MiddlewareMixin):

    def process_request(self, request):

        auth = JWTAuthentication()

        try:
            validated_token = auth.get_validated_token(
                auth.get_raw_token(request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1])
            )

            user = auth.get_user(validated_token)
            request.user = user

            if user and hasattr(user, "clinic") and user.clinic:
                request.clinic = user.clinic
            else:
                request.clinic = None

        except Exception:
            request.clinic = None