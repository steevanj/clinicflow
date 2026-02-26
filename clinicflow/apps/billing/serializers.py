from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["service_name", "quantity", "price", "subtotal"]
        read_only_fields = ["subtotal"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["total_amount", "tax", "clinic"]

    def create(self, validated_data):
        # Extract nested items
        items_data = validated_data.pop("items", [])

        # Create the invoice
        invoice = Invoice.objects.create(**validated_data)

        # Create each item linked to the invoice
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        # Recalculate totals
        invoice.total_amount = sum(
            item.quantity * item.price for item in invoice.items.all()
        )
        invoice.tax = invoice.total_amount * 0.1  # Example: 10% tax
        invoice.save()

        return invoice
