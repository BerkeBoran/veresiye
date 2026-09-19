from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal('0.01')


def calculate_line_totals(quantity_kg: Decimal, unit_price: Decimal, vat_rate: Decimal) -> dict:
    subtotal = quantity_kg * unit_price
    vat = subtotal * (vat_rate / Decimal(100))
    total = subtotal + vat

    return {
        "line_subtotal": subtotal.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "line_vat": vat.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "line_total": total.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    }


def calculate_sale(items: list) -> dict:
    computed_items = []
    subtotal_sum = Decimal(0)
    vat_sum = Decimal(0)
    total_sum = Decimal(0)

    for item in items:
        line = calculate_line_totals(item.quantity_kg, item.unit_price, item.vat_rate)
        computed_items.append({
            "product_name": item.product_name,
            "quantity_kg": item.quantity_kg,
            "unit_price": item.unit_price,
            "vat_rate": item.vat_rate,
            **line
        })
        subtotal_sum += line["line_subtotal"]
        vat_sum += line["line_vat"]
        total_sum += line["line_total"]

    return {
        "items": computed_items,
        "subtotal": subtotal_sum.quantize(TWO_PLACES),
        "vat_amount": vat_sum.quantize(TWO_PLACES),
        "total": total_sum.quantize(TWO_PLACES)
    }
