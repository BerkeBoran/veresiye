from sqlalchemy import Column, Integer, ForeignKey, Date, String, Boolean, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class VehicleExpense(Base):
    __tablename__ = "vehicle_expenses"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    expense_date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    paid_by = Column(String, nullable=False, server_default="us")
    vat_exempt = Column(Boolean, nullable=False, server_default="0")
    vat_rate = Column(Numeric(5,2), nullable=False, server_default="20")
    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    total = Column(Numeric(12,2), nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="vehicle_expenses")