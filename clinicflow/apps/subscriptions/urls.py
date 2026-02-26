# subscriptions/urls.py

from django.urls import path
from .views import (
    PlanListAPIView,
    CurrentSubscriptionAPIView,
    UpgradeSubscriptionAPIView,
)

urlpatterns = [
    path("plans/", PlanListAPIView.as_view(), name="plans"),
    path("current/", CurrentSubscriptionAPIView.as_view(), name="current-subscription"),
    path("upgrade/", UpgradeSubscriptionAPIView.as_view(), name="upgrade-subscription"),
]