from django.urls import path
from .views import (
    CreateInvoiceAPIView,
    InvoiceListAPIView,
    InvoiceDetailAPIView,
)

urlpatterns = [
    path("create/", CreateInvoiceAPIView.as_view()),
    path("", InvoiceListAPIView.as_view()),
    path("<int:id>/", InvoiceDetailAPIView.as_view()),
]