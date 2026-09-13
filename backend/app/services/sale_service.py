

def calculate_sale_totals(quantity_kg: float, unit_price: float, vat_rate: float) -> dict:
    subtotal = quantity_kg * unit_price
    vat_amount = subtotal * (vat_rate / 100)
    total = subtotal + vat_amount

    return {
        "subtotal": round(subtotal, 2),
        "vat_amount": round(vat_amount, 2),
        "total": round(total, 2)
    }
