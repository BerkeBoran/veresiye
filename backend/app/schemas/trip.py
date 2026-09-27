from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, ConfigDict, computed_field



def validate_km_range(start_km: int | None, end_km: int | None) -> None:
    if start_km is not None and end_km is not None and end_km < start_km:
        raise ValueError("Bitiş km'si başlngıç km'sinden küçük olamaz")


class TripBase(BaseModel):
    vehicle_id: int
    trip_date: date
    place_of_shipment: str | None = None
    product_name: str | None = None
    kg: Decimal = Field(ge=0)
    unit_price: Decimal = Field(ge=0)
    vat_exempt: bool = False
    vat_rate: Decimal = Decimal("20")
    start_km: int | None = Field(default=None, ge=0)
    end_km: int | None = Field(default=None, ge=0)
    fuel_liters: Decimal | None = Field(default=None, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def check_km(self):
        validate_km_range(self.start_km, self.end_km)
        return self


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    vehicle_id: int | None = None
    trip_date: date | None = None
    place_of_shipment: str | None = None
    product_name: str | None = None
    kg: Decimal | None = Field(default=None, ge=0)
    unit_price: Decimal | None = Field(default=None, ge=0)
    vat_exempt: bool | None = None
    vat_rate: Decimal | None = None
    start_km: int | None = Field(default=None, ge=0)
    end_km: int | None = Field(default=None, ge=0)
    fuel_liters: Decimal | None = Field(default=None, ge=0)
    notes: str | None = None


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subtotal: Decimal
    vat_amount: Decimal
    total: Decimal
    tevkifat: Decimal
    created_at: datetime

    @computed_field
    @property
    def distance_km(self) -> int | None:
        if self.start_km is None or self.end_km is None:
            return None
        return self.end_km - self.start_km

    @computed_field
    @property
    def liters_per_100km(self) -> Decimal | None:
        distance = self.distance_km
        if not distance or self.fuel_liters is None:
            return None
        return (self.fuel_liters / distance * 100).quantize(Decimal("0.01"))