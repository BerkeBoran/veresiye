import decimal
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal


class PaymentBase(BaseModel):
    customer_id: int
    amount: Decimal
    note: str | None = None
    payment_date: date | None = None
    direction: str = "in"
    payment_type: str = "cash"
    bank_name: str | None = None
    cheque_no: str | None = None
    cheque_due_date: date | None = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    payment_date: date | None
    direction: str
    payment_type: str
    bank_name: str | None
    cheque_no: str | None
    cheque_due_date: date | None

    class Config:
        from_attributes = True


class PaymentUpdate(BaseModel):
    amount: Decimal | None = None
    note: str | None = None
    payment_date: date | None = None
    direction: str | None = None
    payment_type: str | None = None
    bank_name: str | None = None
    cheque_no: str | None = None
    cheque_due_date: date | None = None


class TypeSummary(BaseModel):
    payment_type: str
    incoming: Decimal
    outgoing: Decimal
    net: Decimal


class CaseSummary(BaseModel):
    by_type: list[TypeSummary]
    total_incoming: Decimal
    total_outgoing: Decimal
    net: Decimal
