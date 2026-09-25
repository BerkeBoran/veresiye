from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentRead, ShipmentCreate, ShipmentUpdate
from app.services.shipment_service import calculate_shipment

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.post("/", response_model=ShipmentRead)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == shipment.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    computed = calculate_shipment(
        kg=shipment.kg,
        unit_price=shipment.unit_price,
        vat_rate=shipment.vat_rate,
        vat_exempt=shipment.vat_exempt,
    )

    new_shipment = Shipment(**shipment.model_dump(), **computed)

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment


@router.get("/", response_model=list[ShipmentRead])
def list_shipment(db: Session = Depends(get_db)):
    return db.query(Shipment).all()


@router.delete("/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(shipment)
    db.commit()
    return {"Bilgi": "Nakliye Silindi"}


@router.put("/{shipment_id}", response_model=ShipmentRead)
def update_shipment(shipment_id:int, payload: ShipmentUpdate, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(shipment, field, value)

    computed = calculate_shipment(
        kg=shipment.kg,
        unit_price=shipment.unit_price,
        vat_rate=shipment.vat_rate,
        vat_exempt=shipment.vat_exempt,
    )
    for field, value in computed.items():
        setattr(shipment, field, value)

    db.commit()
    db.refresh(shipment)
    return shipment