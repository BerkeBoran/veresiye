from decimal import Decimal

from app.services.shipment_service import calculate_shipment, to_money

calculate_trip = calculate_shipment


def calculate_expense(total: Decimal, vat_exempt: bool, vat_rate: Decimal) -> dict:

    if vat_exempt:
        vat_amount = Decimal("0.00")
    else:
        vat_amount = to_money(total * vat_rate / (Decimal(100) + vat_rate))

    return {
        "subtotal": total - vat_amount,
        "vat_amount": vat_amount,
    }