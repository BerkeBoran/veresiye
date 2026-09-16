

def calculate_balance(customer) -> dict:
    total_sales = sum(sale.total for sale in customer.sales)
    total_payments = sum(payment.amount for payment in customer.payments)
    balance = total_sales - total_payments

    return {
        "total_sales": round(total_sales),
        "total_payments": round(total_payments),
        "balance": round(balance, 2)
    }