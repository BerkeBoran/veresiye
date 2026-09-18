from datetime import datetime

from pydantic import BaseModel
from decimal import Decimal


class SaleBase(BaseModel):
    customer_id: int
    product_name: str
    quantity_kg: Decimal
    unit_price: Decimal
    vat_rate: Decimal = Decimal(0)


class SaleCreate(SaleBase):
    pass


class SaleRead(SaleBase):
    id: int
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    created_at: datetime

    class Config:
        from_attributes = True