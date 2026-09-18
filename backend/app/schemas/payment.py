import decimal
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal


class PaymentBase(BaseModel):
    customer_id: int
    amount: Decimal
    note: str | None = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
