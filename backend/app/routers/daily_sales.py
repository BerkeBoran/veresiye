from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.daily_sale import DailySale
from app.schemas.daily_sale import DailySaleRead, DailySaleCreate, DailySaleUpdate
from app.services.daily_sale_service import calculate_daily_sale

router = APIRouter(prefix="/daily-sales", tags=["daily-sales"])


@router.post("/", response_model=DailySaleRead)
def create_daily_sale(payload: DailySaleCreate, db: Session = Depends(get_db)):
    computed = calculate_daily_sale(
        kg=payload.kg,
        unit_price=payload.unit_price,
        vat_rate=payload.vat_rate,
        vat_exempt=payload.vat_exempt,
    )

    daily_sale = DailySale(**payload.model_dump(), **computed)

    db.add(daily_sale)
    db.commit()
    db.refresh(daily_sale)
    return daily_sale


@router.get("/", response_model=list[DailySaleRead])
def list_daily_sales(db: Session = Depends(get_db)):
    return (
        db.query(DailySale)
        .order_by(DailySale.sale_date.desc(), DailySale.id.desc())
        .all()
    )


@router.put("/{daily_sale_id}", response_model=DailySaleRead)
def update_daily_sale(daily_sale_id: int, payload: DailySaleUpdate, db: Session = Depends(get_db)):
    daily_sale = db.query(DailySale).filter(DailySale.id == daily_sale_id).first()
    if daily_sale is None:
        raise HTTPException(status_code=404, detail="DailySale not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(daily_sale, field, value)

    computed = calculate_daily_sale(
        kg=daily_sale.kg,
        unit_price=daily_sale.unit_price,
        vat_rate=daily_sale.vat_rate,
        vat_exempt=daily_sale.vat_exempt,
    )
    for field, value in computed.items():
        setattr(daily_sale, field, value)

    db.commit()
    db.refresh(daily_sale)
    return daily_sale


@router.delete("/{daily_sale_id}")
def delete_daily_sale(daily_sale_id: int, db: Session = Depends(get_db)):
    daily_sale = db.query(DailySale).filter(DailySale.id == daily_sale_id).first()
    if daily_sale is None:
        raise HTTPException(status_code=404, detail="DailySale not found")
    db.delete(daily_sale)
    db.commit()
    return {"Bilgi": "Günlük Satış Silindi"}
