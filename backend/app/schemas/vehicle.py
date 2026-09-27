import re
from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict

PLATE_PATTERN = re.compile(r"^(\d{2})\s*([A-Z]{1,3})\s*(\d{2,4})$")


def normalize_plate(value: str) -> str:
    cleaned = " ".join(value.upper().split())
    match = PLATE_PATTERN.match(cleaned)
    if match is None:
        raise ValueError("Geçersiz Plaka")
    return " ".join(match.groups())


class VehicleBase(BaseModel):
    number_plate: str
    notes: str | None = None

    @field_validator("number_plate")
    @classmethod
    def normalize(cls, value: str) -> str:
        return normalize_plate(value)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    number_plate: str | None = None
    notes: str | None = None
    is_active: bool | None = None

    @field_validator("number_plate")
    @classmethod
    def normalize(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return normalize_plate(value)


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime



