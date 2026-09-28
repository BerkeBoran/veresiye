from datetime import date

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.partner_payment import PartnerPayment
from app.models.vehicle import Vehicle
from app.schemas.partner_payment import PartnerPaymentRead, PartnerPaymentCreate, PartnerPaymentUpdate

router = APIRouter(prefix="/partner-payments", tags=["partner-payments"])


def ensure_shared_vehicle(db: Session, vehicle_id: int) -> None:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Araç bulunamadı.")
    if vehicle.partner_name is None:
        raise HTTPException(status_code=400, detail="Bu aracın ortağı bulunmuyor.")


@router.post("/", response_model=PartnerPaymentRead, status_code=201)
def create_partner_payment(payload: PartnerPaymentCreate, db: Session = Depends(get_db)):
    ensure_shared_vehicle(db, payload.vehicle_id)
    partner_payment = PartnerPayment(**payload.model_dump())
    db.add(partner_payment)
    db.commit()
    db.refresh(partner_payment)
    return partner_payment


@router.get("/", response_model=list[PartnerPaymentRead])
def list_partner_payments(vehicle_id: int | None = None, date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    query = db.query(PartnerPayment)
    if vehicle_id is not None:
        query = query.filter(PartnerPayment.vehicle_id == vehicle_id)
    query = filter_by_date_range(query, PartnerPayment.payment_date, date_from, date_to)
    return query.order_by(PartnerPayment.payment_date.desc(), PartnerPayment.id.desc()).all()


@router.patch("/{payment_id}", response_model=PartnerPaymentRead)
def update_partner_payment(payment_id: int, payload: PartnerPaymentUpdate, db: Session = Depends(get_db)):
    partner_payment = db.get(PartnerPayment, payment_id)
    if partner_payment is None:
        raise HTTPException(status_code=404, detail="Ödeme bulunamadı.")

    data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in data:
        ensure_shared_vehicle(db, data["vehicle_id"])
    for field, value in data.items():
        setattr(partner_payment, field, value)
    db.commit()
    db.refresh(partner_payment)
    return partner_payment


@router.delete("/{payment_id}")
def delete_partner_payments(payment_id: int, db: Session = Depends(get_db)):
    partner_payment = db.get(PartnerPayment, payment_id)
    if partner_payment is None:
        raise HTTPException(status_code=404, detail="Ödeme bulunamadı")
    db.delete(partner_payment)
    db.commit()

