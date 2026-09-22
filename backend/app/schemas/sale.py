from datetime import datetime, date

from pydantic import BaseModel, Field
from decimal import Decimal


class SaleCreate(BaseModel):
    customer_id: int
    note: str | None = None
    items: list[SaleItemCreate] = Field(min_length=1)
    document_no: str | None = None
    vat_exempt: bool = False
    transport: bool = False
    transport_price: Decimal | None = None
    transport_vat_rate: Decimal = Decimal(20)
    due_date: date | None = None


class SaleRead(BaseModel):
    id: int
    customer_id: int
    note: str | None
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    created_at: datetime
    items: list[SaleItemRead]
    document_no: str | None
    vat_exempt: bool
    transport: bool
    transport_price: Decimal | None
    transport_vat_rate: Decimal
    transport_tevkifat: Decimal
    transport_vat_amount: Decimal
    transport_total: Decimal
    due_date: date | None

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
    document_no: str | None = None
    vat_exempt: bool = False
    transport: bool = False
    transport_price: Decimal | None = None
    transport_vat_rate: Decimal = Decimal(20)
    due_date: date | None = None
