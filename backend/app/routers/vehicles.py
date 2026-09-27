from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.coercions import expect

from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleRead, VehicleUpdate, VehicleCreate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def get_vehile_or_404(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


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


@router.get("/{vehicle_id}", response_model=list[VehicleRead])
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return get_vehile_or_404(db, vehicle_id)


@router.get("/", response_model=list[VehicleRead])
def list_vehicles(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Vehicle)
    if active_only:
        query = query.filter(Vehicle.is_active.is_(True))
    return query.order_by(Vehicle.is_active.desc(), Vehicle.number_plate).all()


@router.post("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = get_vehile_or_404(db, vehicle_id)
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
    vehicle = get_vehile_or_404(db, vehicle_id)
    if vehicle.trips or vehicle.vehicle_expenses:
        raise HTTPException(status_code=409, detail="Aracın sefer veya gider kaydı var")
    db.delete(vehicle)
    db.commit()
