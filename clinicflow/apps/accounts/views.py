from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .models import User


def standard_response(success, message, data=None):
    return {
        "success": success,
        "message": message,
        "data": data
    }


def get_role_redirect(role):
    mapping = {
        "SUPER_ADMIN": "/super-admin/dashboard",
        "MANAGER": "/manager/dashboard",
        "DOCTOR": "/doctor/dashboard",
        "RECEPTIONIST": "/reception/dashboard",
        "STAFF": "/staff/dashboard",
    }
    return mapping.get(role)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                standard_response(True, "Registration successful"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            standard_response(False, "Validation error", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response(
                standard_response(
                    True,
                    "Login successful",
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "role": user.role,
                        "redirect_url": get_role_redirect(user.role),
                    },
                )
            )
        return Response(
            standard_response(False, "Invalid credentials", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(standard_response(True, "Logged out successfully"))
        except Exception:
            return Response(
                standard_response(False, "Invalid token"),
                status=status.HTTP_400_BAD_REQUEST,
            )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                # In production send via email
                return Response(
                    standard_response(
                        True,
                        "Reset link generated",
                        {"uid": uid, "token": token},
                    )
                )
            except User.DoesNotExist:
                return Response(
                    standard_response(False, "User not found"),
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            standard_response(False, "Validation error", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(standard_response(True, "Password reset successful"))
        return Response(
            standard_response(False, "Invalid reset data", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )