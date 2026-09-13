from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.sale import Sale
from app.schemas.sale import SaleRead, SaleCreate
from app.services.sale_service import calculate_sale_totals

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")


    totals = calculate_sale_totals(sale.quantity_kg, sale.unit_price, sale.vat_rate)

    new_sale = Sale(
        **sale.model_dump(),
        subtotal=totals["subtotal"],
        vat_amount=totals["vat_amount"],
        total=totals["total"]
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@router.get("/", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()