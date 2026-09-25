from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ShipmentBase(BaseModel):
    customer_id: int
    shipment_date: date | None = None
    place_of_shipment: str | None = None
    number_plate: str | None = None
    kg: Decimal
    unit_price: Decimal
    vat_exempt: bool = False
    vat_rate: Decimal = Decimal(20)


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentRead(ShipmentBase):
    model_config =  ConfigDict(from_attributes=True)

    id: int
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    tevkifat: Decimal
    created_at: datetime


class ShipmentUpdate(BaseModel):
    shipment_date: date | None = None
    place_of_shipment: str | None = None
    number_plate: str | None = None
    kg: Decimal | None = None
    unit_price: Decimal | None = None
    vat_exempt: bool | None = None
    vat_rate: Decimal | None = None

