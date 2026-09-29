from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.purchase import PurchaseItem, Purchase
from app.models.supplier import Supplier
from app.schemas.purchase import PurchaseRead, PurchaseCreate, PurchaseUpdate
from app.services.sale_service import calculate_sale

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.post("/", response_model=PurchaseRead)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == purchase.supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")

    computed = calculate_sale(purchase.items, vat_exempt=purchase.vat_exempt)
    new_purchase = Purchase(
        supplier_id=purchase.supplier_id,
        notes=purchase.notes,
        vat_exempt=purchase.vat_exempt,
        subtotal=computed["subtotal"],
        vat_amount=computed["vat_amount"],
        total=computed["total"],
        document_no=purchase.document_no,
        due_date=purchase.due_date,
        purchase_date=purchase.purchase_date
    )

    for item_data in computed["items"]:
        new_purchase.items.append(PurchaseItem(**item_data))

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return new_purchase


@router.get("/", response_model=list[PurchaseRead])
def list_purchases(date_from: date | None = None, date_to: date | None = None, db: Session = Depends(get_db)):
    query = filter_by_date_range(db.query(Purchase), Purchase.purchase_date, date_from, date_to)
    return query.order_by(Purchase.purchase_date.desc(), Purchase.id.desc()).all()


@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Alış işlemi bulunamadı.")
    db.delete(purchase)
    db.commit()
    return {"Bilgi": "Alış silindi."}


@router.put("/{purchase_id}", response_model=PurchaseRead)
def update_purchase(purchase_id: int, payload: PurchaseUpdate, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase is None:
        raise HTTPException(status_code=404, detail="Alış işlemi bulunamadı.")

    purchase.items.clear()
    computed = calculate_sale(payload.items, vat_exempt=payload.vat_exempt)
    purchase.notes = payload.notes
    purchase.vat_exempt = payload.vat_exempt
    purchase.subtotal = computed["subtotal"]
    purchase.vat_amount = computed["vat_amount"]
    purchase.total = computed["total"]
    purchase.document_no = payload.document_no
    purchase.due_date = payload.due_date
    purchase.purchase_date = payload.purchase_date

    for item_data in computed["items"]:
        purchase.items.append(PurchaseItem(**item_data))

    db.commit()
    db.refresh(purchase)
    return purchase