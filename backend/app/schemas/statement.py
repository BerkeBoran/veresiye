from pydantic import BaseModel

from app.schemas.customer import CustomerRead
from app.schemas.payment import PaymentRead
from app.schemas.sale import SaleRead
from decimal import Decimal


class CustomerStatement(BaseModel):
    customer: CustomerRead
    total_sales: Decimal
    total_payments: Decimal
    balance: Decimal
    sales: list[SaleRead]
    payments: list[PaymentRead]