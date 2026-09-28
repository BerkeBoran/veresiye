from datetime import date

from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.core.filters import filter_by_date_range
from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.vehicle_expense import VehicleExpense
from app.schemas.vehicle_expense import VehicleExpenseRead, VehicleExpenseCreate, ExpenseCategory, VehicleExpenseUpdate
from app.services.vehicle_service import calculate_expense

router = APIRouter(prefix="/vehicle-expenses", tags=["vehicle-expenses"])


def ensure_vehicle(db: Session, vehicle_id: int ):
    if db.get(Vehicle, vehicle_id) is None:
        raise HTTPException(status_code=404, detail="Araç bulunamadı.")


def apply_expense_totals(expense: VehicleExpense) -> None:
    computed = calculate_expense(
        total=expense.total,
        vat_rate=expense.vat_rate,
        vat_exempt=expense.vat_exempt,
    )
    for field, value in computed.items():
        setattr(expense, field, value)


def check_partner(db: Session, vehicle_id: int, paid_by: str):
    if paid_by == "partner":
        vehicle = db.get(Vehicle, vehicle_id)
        if vehicle is not None and vehicle.partner_name is None:
            raise HTTPException(status_code=400, detail="Bu aracın ortağı yok")


@router.post("/", response_model=VehicleExpenseRead, status_code=201)
def create_expense(payload: VehicleExpenseCreate, db: Session = Depends(get_db)):
    ensure_vehicle(db, payload.vehicle_id)
    check_partner(db, payload.vehicle_id, payload.paid_by)
    expense = VehicleExpense(**payload.model_dump())
    apply_expense_totals(expense)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/", response_model=list[VehicleExpenseRead])
def list_expenses(
        vehicle_id: int | None = None,
        category: ExpenseCategory | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        db: Session = Depends(get_db)):
    query = db.query(VehicleExpense)
    if vehicle_id is not None:
        query = query.filter(VehicleExpense.vehicle_id == vehicle_id)
    if category is not None:
        query = query.filter(VehicleExpense.category == category)
    query = filter_by_date_range(query, VehicleExpense.expense_date, date_from, date_to)
    return query.order_by(VehicleExpense.expense_date.desc(), VehicleExpense.id.desc()).all()


@router.patch("/{expense_id}", response_model=VehicleExpenseRead)
def update_expense(expense_id: int, payload: VehicleExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.get(VehicleExpense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Harcama bulunamadı")

    data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in data:
        ensure_vehicle(db, data["vehicle_id"])
    for field, value in data.items():
        setattr(expense, field, value)

    check_partner(db, expense.vehicle_id, expense.paid_by)

    apply_expense_totals(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(VehicleExpense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Harcama bulunamadı")
    db.delete(expense)
    db.commit()