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


def calculate_vehicle_summary(trips: list, expenses: list, partnet_payments: list) -> dict:
    total_income = sum((trip.total for trip in trips), Decimal(0))
    total_expense = sum((expense.total for expense in expenses), Decimal(0))
    net = total_income - total_expense

    our_expense = sum((expense.total for expense in expenses if expense.paid_by == "us"), Decimal(0))
    partner_expense = sum((expense.total for expense in expenses if expense.paid_by == "partner"), Decimal(0))
    partner_payments_total = sum((payment.amount for payment in partnet_payments), Decimal(0))

    total_kg = sum((trip.kg for trip in trips), Decimal(0))

    measured_trips = [
        trip for trip in trips
        if trip.start_km is not None and trip.end_km is not None and trip.fuel_liters is not None
    ]
    total_km = sum(trip.end_km - trip.start_km for trip in measured_trips)
    total_liters = sum((trip.fuel_liters for trip in measured_trips), Decimal(0))

    if total_km > 0:
        liters_per_100km = (total_liters / total_km * 100).quantize(Decimal("0.01"))
    else:
        liters_per_100km = None

    expenses_by_category = {}
    for expense in expenses:
        if expense.category not in expenses_by_category:
            expenses_by_category[expense.category] = Decimal(0)
        expenses_by_category[expense.category] += expense.total

    return {
        "trip_count": len(trips),
        "total_kg": total_kg,
        "total_km": total_km,
        "total_liters": total_liters,
        "liters_per_100km": liters_per_100km,
        "total_income": total_income.quantize(Decimal("0.01")),
        "total_expense": total_expense.quantize(Decimal("0.01")),
        "net": net.quantize(Decimal("0.01")),
        "expenses_by_category": expenses_by_category,
        "our_expense": our_expense.quantize(Decimal("0.01")),
        "partner_expense": partner_expense.quantize(Decimal("0.01")),
        "partner_payments_total": partner_payments_total.quantize(Decimal("0.01")),
    }

