from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal('0.01')
TEVKIFAT_ESIK = Decimal("12000")


def calculate_line_totals(quantity_kg: Decimal, unit_price: Decimal, vat_rate: Decimal) -> dict:
    subtotal = quantity_kg * unit_price
    vat = subtotal * (vat_rate / Decimal(100))
    total = subtotal + vat

    return {
        "line_subtotal": subtotal.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "line_vat": vat.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
        "line_total": total.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    }


def calculate_sale(items: list, vat_exempt: bool = False, transport: bool = False, transport_price: Decimal = None, transport_vat_rate: Decimal = Decimal(20)) -> dict:
    computed_items = []
    subtotal_sum = Decimal(0)
    vat_sum = Decimal(0)
    total_sum = Decimal(0)

    for item in items:
        rate = Decimal(0) if vat_exempt else item.vat_rate
        line = calculate_line_totals(item.quantity_kg, item.unit_price, rate)
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

    if transport:
        t = calculate_transport(transport_price, apply_vat= not vat_exempt, vat_rate=transport_vat_rate)

    else:
        t = {"net": Decimal(0), "tevkifat": Decimal(0), "vat": Decimal(0)}

    return {
        "items": computed_items,
        "subtotal": subtotal_sum.quantize(TWO_PLACES),
        "vat_amount": vat_sum.quantize(TWO_PLACES),
        "total": (total_sum + t["net"]).quantize(TWO_PLACES),
        "transport_tevkifat": t["tevkifat"],
        "transport_total": t["net"],
        "transport_vat_amount": t["vat"],
    }


def calculate_transport(price, apply_vat: bool, vat_rate) -> dict:
    if not price or price <= 0:
        return {"net": Decimal(0), "tevkifat": Decimal(0), "vat": Decimal(0)}

    vat = price * vat_rate / Decimal(100) if apply_vat else Decimal(0)
    vat_included = price + vat
    if apply_vat and vat_included > TEVKIFAT_ESIK:
        tevkifat = vat * Decimal(2) / Decimal(10)
    else:
        tevkifat = Decimal(0)
    net = vat_included - tevkifat
    return {
        "net": net.quantize(TWO_PLACES),
        "tevkifat": tevkifat.quantize(TWO_PLACES),
        "vat": vat.quantize(TWO_PLACES),
    }
