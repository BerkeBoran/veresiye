from decimal import Decimal

TWO_PLACES = Decimal('0.01')

def calculate_balance(customer) -> dict:
    total_sales = sum((sale.total for sale in customer.sales), Decimal(0))
    total_payments = sum((payment.amount for payment in customer.payments), Decimal(0))
    balance = total_sales - total_payments

    return {
        "total_sales": total_sales.quantize(TWO_PLACES),
        "total_payments": total_payments.quantize(TWO_PLACES),
        "balance": balance.quantize(TWO_PLACES)
    }