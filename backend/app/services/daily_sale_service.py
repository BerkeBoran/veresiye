from decimal import Decimal

from app.services.sale_service import calculate_line_totals


def calculate_daily_sale(kg: Decimal, unit_price: Decimal, vat_exempt: bool, vat_rate: Decimal) -> dict:
    rate = Decimal(0) if vat_exempt else vat_rate
    line = calculate_line_totals(kg, unit_price, rate)

    return {
        "subtotal": line["line_subtotal"],
        "vat_amount": line["line_vat"],
        "total": line["line_total"],
    }