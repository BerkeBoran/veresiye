from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DailySaleBase(BaseModel):
    sale_date: date
    place_of_shipment: str | None = None
    number_plate: str | None = None
    product_name: str | None = None
    kg: Decimal
    unit_price: Decimal
    vat_exempt: bool = False
    vat_rate: Decimal = Decimal("20")


class DailySaleCreate(DailySaleBase):
    pass


class DailySaleRead(DailySaleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    created_at: datetime


class DailySaleUpdate(BaseModel):
    sale_date: date | None = None
    place_of_shipment: str | None = None
    number_plate: str | None = None
    product_name: str | None = None
    kg: Decimal | None = None
    unit_price: Decimal | None = None
    vat_exempt: bool | None = None
    vat_rate: Decimal | None = None