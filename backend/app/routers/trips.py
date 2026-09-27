from datetime import date

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.trip import TripCreate, TripRead, validate_km_range, TripUpdate
from app.services.vehicle_service import calculate_trip

router = APIRouter(prefix="/trips", tags=["trips"])


def ensure_vehicle(db: Session, vehicle_id: int) -> None:
    if db.get(Vehicle, vehicle_id) is None:
        raise HTTPException(status_code=404, detail="Araç Bulunamadı")


def apply_trip_totals(trip: Trip) -> None:
    computed = calculate_trip(
        kg=trip.kg,
        unit_price=trip.unit_price,
        vat_rate=trip.vat_rate,
        vat_exempt=trip.vat_exempt,
    )
    for field, value in computed.items():
        setattr(trip, field, value)


@router.post("/", response_model=TripRead, status_code=201)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    ensure_vehicle(db, payload.vehicle_id)
    trip = Trip(**payload.model_dump())
    apply_trip_totals(trip)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("/", response_model=list[TripRead])
def list_trips(vehicle_id: int | None = None, date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    query = db.query(Trip)
    if vehicle_id is not None:
        query = query.filter(Trip.vehicle_id == vehicle_id)
    query = filter_by_date_range(query, Trip.trip_date, date_from, date_to)
    return query.order_by(Trip.trip_date.desc(), Trip.id.desc()).all()


@router.patch("/{trip_id}", response_model=TripRead)
def update_trip(trip_id: int, payload: TripUpdate, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Sefer bulunamadı.")

    data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in data:
        ensure_vehicle(db, data["vehicle_id"])
    for field, value in data.items():
        setattr(trip, field, value)

    try:
        validate_km_range(trip.start_km, trip.end_km)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    apply_trip_totals(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Sefer bulunamadı.")
    db.delete(trip)
    db.commit()
    return {"Bilgi": "Sefer Silindi"}
