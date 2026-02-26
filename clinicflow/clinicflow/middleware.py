from django.utils.deprecation import MiddlewareMixin


class ClinicIsolationMiddleware(MiddlewareMixin):
    """
    Ensures every request is scoped to a clinic.
    Expects authenticated user with clinic attribute.
    """

    def process_request(self, request):
        user = request.user

        if user.is_authenticated:
            request.clinic = getattr(user, "clinic", None)
        else:
            request.clinic = None