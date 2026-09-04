from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str | None = None
    surname: str | None = None
    company_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    tax_number: str | None = None
    notes: str | None = None
    address: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    class Config:
        from_attributes = True