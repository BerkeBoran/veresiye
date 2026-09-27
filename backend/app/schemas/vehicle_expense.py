from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import Field, BaseModel, ConfigDict

ExpenseCategory = Literal["fuel", "maintenance", "tire", "insurance", "inspection", "tax", "toll", "driver", "other"]


class VehicleExpenseBase(BaseModel):
    vehicle_id: int
    expense_date: date
    category: ExpenseCategory
    total: Decimal = Field(gt=0, decimal_places=2)
    vat_exempt: bool = False
    vat_rate: Decimal = Decimal("20")
    notes: str | None = None


class VehicleExpenseCreate(VehicleExpenseBase):
    pass


class VehicleExpenseUpdate(BaseModel):
    vehicle_id: int | None = None
    expense_date: date | None = None
    category: ExpenseCategory | None = None
    total: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    vat_exempt: bool | None = None
    vat_rate: Decimal | None = None
    notes: str | None = None


class VehicleExpenseRead(VehicleExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subtotal: Decimal
    vat_amount: Decimal
    created_at: datetime