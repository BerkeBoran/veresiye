from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.responses import Response

from app.database import get_db
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.sale import Sale
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate, CustomerWithBalance
from app.schemas.statement import CustomerStatement
from app.services.customer_service import calculate_balance
from app.services.export_service import build_statement_excel

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


@router.get("/balances", response_model=list[CustomerWithBalance])
def customer_with_balances(db: Session = Depends(get_db)):
    sales_by_customer = dict(
        db.query(Sale.customer_id, func.sum(Sale.total))
        .group_by(Sale.customer_id)
        .all()
    )

    payments_by_customer = dict(
        db.query(Payment.customer_id, func.sum(Payment.amount))
        .filter(Payment.direction == "in")
        .group_by(Payment.customer_id)
        .all()
    )

    result = []
    for customer in db.query(Customer).all():
        total_sales = sales_by_customer.get(customer.id, Decimal(0))
        total_payments = payments_by_customer.get(customer.id, Decimal(0))
        result.append(
            CustomerWithBalance(
                **CustomerRead.model_validate(customer).model_dump(),
                total_sales=total_sales,
                total_payments=total_payments,
                balance=total_sales - total_payments,
            )
        )
    return result


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


@router.get("/{customer_id}/balance")
def get_customer_balance(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")

    result = calculate_balance(customer)
    return {
        "customer_id": customer_id,
        **result
    }


@router.get("/{customer_id}/statement", response_model=CustomerStatement)
def get_customer_statement(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")

    totals = calculate_balance(customer)
    return {
        "customer": customer,
        "total_sales": totals["total_sales"],
        "total_payments": totals["total_payments"],
        "balance": totals["balance"],
        "sales": customer.sales,
        "payments": [payments for payments in customer.payments if payments.direction == "in" ]
    }


@router.get("/{customer_id}/statement/excel")
def statement_excel(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return HTTPException(status_code=404, detail="Customer not found")

    totals = calculate_balance(customer)
    content = build_statement_excel(customer, customer.sales, customer.payments, totals)

    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="ekstre_{customer_id}.xlsx"'},
    )



