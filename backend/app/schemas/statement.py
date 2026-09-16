from pydantic import BaseModel

from app.schemas.customer import CustomerRead
from app.schemas.payment import PaymentRead
from app.schemas.sale import SaleRead


class CustomerStatement(BaseModel):
    customer = CustomerRead
    total_sales: float
    total_payments: float
    balance: float
    sales = list[SaleRead]
    payments = list[PaymentRead]