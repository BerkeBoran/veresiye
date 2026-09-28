from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    number_plate = Column(String, nullable=False, unique=True)
    notes = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    partner_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    trips = relationship("Trip", back_populates="vehicle")
    vehicle_expenses = relationship("VehicleExpense", back_populates="vehicle")
    partner_payments = relationship("PartnerPayment", back_populates="vehicle")

