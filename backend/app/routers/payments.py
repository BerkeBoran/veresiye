from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.payment import Payment
from app.schemas.payment import PaymentRead, PaymentCreate

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
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


