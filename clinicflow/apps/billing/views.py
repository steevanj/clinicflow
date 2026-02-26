from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib import pagesizes

from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer
from .services import calculate_invoice_totals
from .permissions import IsManager

from io import BytesIO


class CreateInvoiceAPIView(APIView):

    def post(self, request):
        data = request.data
        items_data = data.pop("items")

        subtotal, tax, total = calculate_invoice_totals(items_data)

        invoice = Invoice.objects.create(
            clinic=request.user.clinic,
            patient_id=data["patient"],
            doctor_id=data["doctor"],
            payment_method=data["payment_method"],
            tax=tax,
            total_amount=total,
        )

        for item in items_data:
            InvoiceItem.objects.create(
                invoice=invoice,
                service_name=item["service_name"],
                quantity=item["quantity"],
                price=item["price"],
                subtotal=item["subtotal"],
            )

        return Response({"message": "Invoice created"}, status=201)


class InvoiceListAPIView(APIView):

    def get(self, request):
        invoices = Invoice.objects.filter(clinic=request.user.clinic)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)


class InvoiceDetailAPIView(APIView):

    def get(self, request, id):
        invoice = get_object_or_404(
            Invoice, id=id, clinic=request.user.clinic
        )
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def delete(self, request, id):
        if request.user.role != "manager":
            return Response({"error": "Only Manager can delete."}, status=403)

        invoice = get_object_or_404(
            Invoice, id=id, clinic=request.user.clinic
        )
        invoice.delete()
        return Response({"message": "Deleted"}, status=204)
    
    def post(self, request, id):
        invoice = get_object_or_404(
            Invoice, id=id, clinic=request.user.clinic
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"Invoice #{invoice.id}", styles["Title"]))
        elements.append(Spacer(1, 12))

        data = [["Service", "Qty", "Price", "Subtotal"]]

        for item in invoice.items.all():
            data.append([
                item.service_name,
                str(item.quantity),
                str(item.price),
                str(item.subtotal),
            ])

        table = Table(data)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        elements.append(table)
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Tax: {invoice.tax}", styles["Normal"]))
        elements.append(Paragraph(f"Total: {invoice.total_amount}", styles["Normal"]))

        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(
            buffer,
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="invoice_{invoice.id}.pdf"'
            },
        )