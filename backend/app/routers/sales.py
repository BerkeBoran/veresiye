from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleRead, SaleCreate
from app.services.sale_service import calculate_sale

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")


    computed = calculate_sale(sale.items)

    new_sale = Sale(
        customer_id=sale.customer_id,
        note=sale.note,
        subtotal=computed["subtotal"],
        vat_amount=computed["vat_amount"],
        total=computed["total"]
    )

    for item_data in computed["items"]:
        new_sale.items.append(SaleItem(**item_data))

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@router.get("/", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()