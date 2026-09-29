from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.models.purchase import Purchase
from app.models.supplier import Supplier
from app.schemas.statement import SupplierStatement
from app.schemas.supplier import SupplierRead, SupplierCreate, SupplierWithBalance, SupplierUpdate
from app.services.supplier_service import calculate_supplier_balance

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/", response_model=SupplierRead)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    new_supplier = Supplier(**supplier.model_dump())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier


@router.get("/", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()


@router.get("/balances", response_model=list[SupplierWithBalance])
def supplier_with_balance(db: Session = Depends(get_db)):
    purchases_by_supplier = dict(
        db.query(Purchase.supplier_id, func.sum(Purchase.total))
        .group_by(Purchase.supplier_id)
        .all()
    )
    payments_by_supplier = dict(
        db.query(Payment.supplier_id, func.sum(Payment.amount))
        .filter(Payment.direction == "out")
        .group_by(Payment.supplier_id)
        .all()
    )

    result = []
    for supplier in db.query(Supplier).all():
        total_purchases = purchases_by_supplier.get(supplier.id, Decimal(0))
        total_payments = payments_by_supplier.get(supplier.id, Decimal(0))
        result.append(
            SupplierWithBalance(
                **SupplierRead.model_validate(supplier).model_dump(),
                total_purchases=total_purchases,
                total_payments=total_payments,
                balance=total_purchases - total_payments
            )
        )
    return result


@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")
    return supplier


@router.patch("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: int, supplier_update: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")
    for field, value in supplier_update.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")
    if supplier.purchases or supplier.payments:
        raise HTTPException(status_code=409, detail="Tedarikçinin alış veya ödeme kaydı var.")
    db.delete(supplier)
    db.commit()
    return {"Bilgi": "Tedarikçi Silindi"}


@router.get("/{supplier_id}/balance")
def get_supplier_balance(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")
    result = calculate_supplier_balance(supplier)
    return (
        {
            "supplier_id": supplier_id,
            **result
        }
    )


@router.get("/{supplier_id}/statement", response_model=SupplierStatement)
def get_supplier_statement(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Tedarikçi bulunamadı.")
    totals = calculate_supplier_balance(supplier)
    return {
        "supplier": supplier,
        "total_purchases": totals["total_purchases"],
        "total_payments": totals["total_payments"],
        "balance": totals["balance"],
        "purchases": supplier.purchases,
        "payments": [payment for payment in supplier.payments if payment.direction == "out"]
    }
