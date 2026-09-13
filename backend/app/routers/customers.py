from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate

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


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.patch("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")

    for field, value in customer_update.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return customer