from decimal import Decimal

TAX_PERCENTAGE = Decimal("0.18")  # 18% GST


def calculate_invoice_totals(items):
    subtotal_total = Decimal("0.00")

    for item in items:
        subtotal = Decimal(item["price"]) * item["quantity"]
        subtotal_total += subtotal
        item["subtotal"] = subtotal

    tax = subtotal_total * TAX_PERCENTAGE
    total = subtotal_total + tax

    return subtotal_total, tax, total