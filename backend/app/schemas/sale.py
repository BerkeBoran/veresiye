from datetime import datetime

from pydantic import BaseModel, Field
from decimal import Decimal


class SaleCreate(BaseModel):
    customer_id: int
    note: str | None = None
    items: list[SaleItemCreate] = Field(min_length=1)


class SaleRead(BaseModel):
    id: int
    customer_id: int
    note: str | None
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    created_at: datetime
    items: list[SaleItemRead]

    class Config:
        from_attributes = True


class SaleItemCreate(BaseModel):
    product_name: str
    quantity_kg: Decimal
    unit_price: Decimal
    vat_rate: Decimal = Decimal(0)


class SaleItemRead(BaseModel):
    id: int
    product_name: str
    quantity_kg: Decimal
    unit_price: Decimal
    vat_rate: Decimal
    line_subtotal: Decimal
    line_total: Decimal
    line_vat: Decimal


class SaleUpdate(BaseModel):
    note: str | None = None
    items: list[SaleItemCreate] = Field(min_length=1)

