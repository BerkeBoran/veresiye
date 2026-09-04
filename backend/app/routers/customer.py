from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.get("/", response_model=list[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()