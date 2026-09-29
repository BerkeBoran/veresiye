from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PurchaseItemCreate(BaseModel):
    product_name: str
    quantity_kg: Decimal
    unit_price: Decimal
    vat_rate: Decimal = Decimal(0)


class PurchaseItemRead(BaseModel):
    id: int
    product_name: str
    quantity_kg: Decimal
    unit_price: Decimal
    vat_rate: Decimal
    line_subtotal: Decimal
    line_total: Decimal
    line_vat: Decimal


class PurchaseCreate(BaseModel):
    items: list[PurchaseItemCreate] = Field(min_length=1)
    supplier_id: int
    notes: str | None = None
    document_no: str | None = None
    vat_exempt: bool = False
    due_date: date | None = None
    purchase_date: date | None = None


class PurchaseRead(BaseModel):
    id: int
    supplier_id: int
    notes: str | None
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    created_at: datetime
    items: list[PurchaseItemRead]
    document_no: str | None
    vat_exempt: bool
    due_date: date | None
    purchase_date: date | None

    class Config:
        from_attributes = True


class PurchaseUpdate(BaseModel):
    notes: str | None = None
    vat_exempt: bool | None = None
    due_date: date | None = None
    purchase_date: date | None = None
    items: list[PurchaseItemCreate] = Field(min_length=1)
    document_no: str | None = None

