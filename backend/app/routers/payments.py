from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.supplier import Supplier
from app.schemas.payment import PaymentRead, PaymentCreate, PaymentUpdate, CaseSummary, TypeSummary

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    if payment.customer_id is None and payment.supplier_id is None:
        raise HTTPException(status_code=400, detail="Ödeme bir müşteriye ya da tedarikçiye ait olmalı.")

    if payment.customer_id is not None and payment.supplier_id is not None:
        raise HTTPException(status_code=400, detail="Ödeme aynı anda hem müşteriye hemde tedarikçiye ait olamaz.")

    if payment.customer_id is not None:
        customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
        if customer is None:
            raise HTTPException(status_code=404, detail="Müşteri bulunamadı.")

    if payment.supplier_id is not None:
        supplier = db.query(Supplier).filter(Supplier.id == payment.supplier_id).first()
        if supplier is None:
            raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")

    new_payment = Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/", response_model=list[PaymentRead])
def get_payments(direction: str | None = None, date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    query = db.query(Payment)
    if direction:
        query = query.filter(Payment.direction == direction)
    query = filter_by_date_range(query, Payment.payment_date, date_from, date_to)
    return query.order_by(Payment.payment_date.desc(), Payment.id.desc()).all()


@router.get("/summary", response_model=CaseSummary)
def payments_summary(db: Session = Depends(get_db)):
    types = ["cash", "transfer", "cheque"]
    by_type = []
    total_in = Decimal(0)
    total_out = Decimal(0)
    for type in types:
        incoming = db.query(func.coalesce(func.sum(Payment.amount),0)).filter(Payment.payment_type == type, Payment.direction == "in").scalar()
        outgoing = db.query(func.coalesce(func.sum(Payment.amount),0)).filter(Payment.payment_type == type, Payment.direction == "out").scalar()
        by_type.append(TypeSummary(payment_type=type, incoming=incoming, outgoing=outgoing, net=incoming - outgoing))
        total_in += incoming
        total_out += outgoing

    return CaseSummary(by_type=by_type, total_incoming=total_in, total_outgoing=total_out, net=total_in - total_out)




@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"Bilgi": "Tahsilat Silindi"}


@router.patch("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    for field, value in payment_update.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)
    return payment
