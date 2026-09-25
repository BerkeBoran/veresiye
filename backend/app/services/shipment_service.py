from decimal import Decimal, ROUND_HALF_UP


TWO_PLACES = Decimal('0.01')
TEVKIFAT_ESIK = Decimal("12000")
TEVKIFAT_ORANI = Decimal(2) / Decimal(10)

def to_money(value: Decimal) -> Decimal:
    return value.quantize(TWO_PLACES, rounding='ROUND_HALF_UP')


def calculate_shipment(kg: Decimal, unit_price: Decimal, vat_exempt: bool, vat_rate: Decimal) -> dict:
    subtotal = to_money(kg * unit_price)

    if vat_exempt:
        vat_amount = Decimal(0)
    else:
        vat_amount = to_money(subtotal * vat_rate / Decimal(100))

    vat_included = subtotal + vat_amount

    if not vat_exempt and vat_included > TEVKIFAT_ESIK:
        tevkifat = to_money(vat_amount * TEVKIFAT_ORANI)
    else:
        tevkifat = Decimal(0)

    total = to_money(vat_included - tevkifat)

    return {
        "subtotal": subtotal,
        "vat_amount": vat_amount,
        "tevkifat": tevkifat,
        "total": total
    }
