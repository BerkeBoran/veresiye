from decimal import Decimal

from pydantic import BaseModel


class SupplierBase(BaseModel):
    name: str
    surname: str | None = None
    company_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    tax_number: str | None = None
    notes: str | None = None
    address: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    company_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    tax_number: str | None = None
    notes: str | None = None
    address: str | None = None


class SupplierRead(SupplierBase):
    id: int

    class Config:
        from_attributes = True


class SupplierWithBalance(SupplierRead):
    total_purchases: Decimal
    total_payments: Decimal
    balance: Decimal