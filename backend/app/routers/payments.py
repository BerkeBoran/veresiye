from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.payment import Payment
from app.schemas.payment import PaymentRead, PaymentCreate, PaymentUpdate, CaseSummary, TypeSummary

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_payment = Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/", response_model=list[PaymentRead])
def get_payments(direction: str | None = None,db: Session = Depends(get_db)):
    db.query(Payment).all()
    if direction:
        return db.query(Payment).filter(Payment.direction == direction).all()
    return db.query(Payment).all()


@router.get("/{summary}", response_model=CaseSummary)
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
