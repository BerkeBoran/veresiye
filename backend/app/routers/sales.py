from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleRead, SaleCreate, SaleUpdate
from app.services.sale_service import calculate_sale

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")


    computed = calculate_sale(sale.items, vat_exempt=sale.vat_exempt, transport=sale.transport, transport_price=sale.transport_price, transport_vat_rate=sale.transport_vat_rate)

    new_sale = Sale(
        customer_id=sale.customer_id,
        note=sale.note,
        vat_exempt=sale.vat_exempt,
        subtotal=computed["subtotal"],
        vat_amount=computed["vat_amount"],
        total=computed["total"],
        document_no=sale.document_no,
        transport = sale.transport,
        transport_price=sale.transport_price,
        transport_vat_rate=sale.transport_vat_rate,
        transport_tevkifat=computed["transport_tevkifat"],
        transport_total=computed["transport_total"],
        transport_vat_amount=computed["transport_vat_amount"],

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


@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        return HTTPException(status_code=404, detail="Sale not found")
    db.delete(sale)
    db.commit()
    return {"Bilgi": "Satış Silindi"}


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: int, payload: SaleUpdate, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        return HTTPException(status_code=404, detail="Sale not found")

    sale.items.clear()
    computed = calculate_sale(payload.items, vat_exempt=payload.vat_exempt)
    sale.note = payload.note
    sale.document_no = payload.document_no
    sale.vat_exempt = payload.vat_exempt
    sale.transport = payload.transport
    sale.transport_price = payload.transport_price
    sale.transport_vat_rate = payload.transport_vat_rate
    sale.transport_tevkifat = computed["transport_tevkifat"]
    sale.subtotal = computed["subtotal"]
    sale.vat_amount = computed["vat_amount"]
    sale.total = computed["total"]
    sale.transport_vat_amount = computed["transport_vat_amount"]
    sale.transport_total = computed["transport_total"]

    for item_data in computed["items"]:
        sale.items.append(SaleItem(**item_data))

    db.commit()
    db.refresh(sale)
    return sale