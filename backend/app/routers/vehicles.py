from datetime import date

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.vehicle_expense import VehicleExpense
from app.schemas.vehicle import VehicleRead, VehicleUpdate, VehicleCreate
from app.services.vehicle_service import calculate_vehicle_summary

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def get_vehicle_or_404(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


def load_vehicle_records(db: Session, vehicle_id: int, date_from: date | None, date_to: date | None):
    trips_query = db.query(Trip).filter(Trip.vehicle_id == vehicle_id)
    trips = filter_by_date_range(trips_query, Trip.trip_date, date_from, date_to).all()

    expenses_query = db.query(VehicleExpense).filter(VehicleExpense.vehicle_id == vehicle_id)
    expenses = filter_by_date_range(expenses_query, VehicleExpense.expense_date, date_from, date_to).all()

    return trips, expenses



@router.post("/", response_model=VehicleRead, status_code=201)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"{payload.number_plate} plakalı araç zaten kayıtlı.")
    db.refresh(vehicle)
    return vehicle


@router.get("/summary")
def fleet_summary(date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).order_by(Vehicle.number_plate).all()
    result = []
    for vehicle in vehicles:
        trips, expenses = load_vehicle_records(db, vehicle.id, date_from, date_to)
        summary = calculate_vehicle_summary(trips, expenses)
        result.append({
            "vehicle_id": vehicle.id,
            "number_plate": vehicle.number_plate,
            "is_active": vehicle.is_active,
            **summary
        })
    return result


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return get_vehicle_or_404(db, vehicle_id)


@router.get("/", response_model=list[VehicleRead])
def list_vehicles(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Vehicle)
    if active_only:
        query = query.filter(Vehicle.is_active.is_(True))
    return query.order_by(Vehicle.is_active.desc(), Vehicle.number_plate).all()


@router.get("/{vehicle_id}/summary")
def vehicle_summary(vehicle_id: int, date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    vehicle = get_vehicle_or_404(db, vehicle_id)
    trips, expenses = load_vehicle_records(db, vehicle.id, date_from, date_to)
    summary = calculate_vehicle_summary(trips, expenses)
    return {"vehicle_id": vehicle.id, "number_plate": vehicle.number_plate, **summary,}


@router.patch("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = get_vehicle_or_404(db, vehicle_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Bu plaka başka bir araçta kayıtlı.")
    db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = get_vehicle_or_404(db, vehicle_id)
    if vehicle.trips or vehicle.vehicle_expenses:
        raise HTTPException(status_code=409, detail="Aracın sefer veya gider kaydı var")
    db.delete(vehicle)
    db.commit()
