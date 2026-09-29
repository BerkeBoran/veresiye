from decimal import Decimal


def calculate_supplier_balance(supplier) -> dict:
    total_purchases = sum((purchase.total for purchase in supplier.purchases), Decimal(0))
    total_payments = sum((payment.amount for payment in supplier.payments if payment.direction == "out"), Decimal(0))
    balance = total_purchases - total_payments

    return {
        "total_purchases": total_purchases.quantize(Decimal("0.01")),
        "total_payments": total_payments.quantize(Decimal("0.01")),
        "balance": balance.quantize(Decimal("0.01")),
    }