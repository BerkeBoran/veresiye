from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class PartnerPaymentBase(BaseModel):
    vehicle_id: int
    payment_date: date
    amount: Decimal = Field(gt=0, decimal_places=2)
    notes: str | None = None


class PartnerPaymentCreate(PartnerPaymentBase):
    pass


class PartnerPaymentUpdate(BaseModel):
    vehicle_id: int | None = None
    payment_date: date | None = None
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    notes: str | None = None


class PartnerPaymentRead(PartnerPaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime