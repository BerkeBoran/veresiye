from datetime import datetime

from pydantic import BaseModel


class SaleBase(BaseModel):
    customer_id: int
    product_name: str
    quantity_kg: float
    unit_price: float
    vat_rate: float = 0


class SaleCreate(SaleBase):
    pass


class SaleRead(SaleBase):
    id: int
    subtotal: float
    vat_amount: float
    total: float
    created_at: datetime

    class Config:
        from_attributes = True