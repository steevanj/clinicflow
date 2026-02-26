# tenants/urls.py

from django.urls import path
from .views import ClinicMeView, ClinicUpdateView, ClinicListView

urlpatterns = [
    path("me/", ClinicMeView.as_view(), name="clinic-me"),
    path("update/", ClinicUpdateView.as_view(), name="clinic-update"),
    path("all/", ClinicListView.as_view(), name="clinic-list"),
]