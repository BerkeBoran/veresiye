from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal('0.01')


def calculate_sale_totals(quantity_kg: Decimal, unit_price: Decimal, vat_rate: Decimal) -> dict:
    subtotal = quantity_kg * unit_price
    vat_amount = subtotal * (vat_rate / Decimal(100))
    total = subtotal + vat_amount

    return {
        "subtotal": subtotal.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "vat_amount": vat_amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "total": total.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    }
