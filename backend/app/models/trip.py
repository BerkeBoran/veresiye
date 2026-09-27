from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    trip_date = Column(Date, nullable=False)
    place_of_shipment = Column(String, nullable=True)
    product_name = Column(String, nullable=True)
    kg = Column(Numeric(10,3), nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    vat_exempt = Column(Boolean, nullable=False, server_default="0")
    vat_rate = Column(Numeric(5,2), nullable=False, server_default="20")
    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    tevkifat = Column(Numeric(12,2), nullable=False, server_default="0")
    total = Column(Numeric(12,2), nullable=False)
    start_km = Column(Integer, nullable=True)
    end_km = Column(Integer, nullable=True)
    fuel_liters = Column(Numeric(10,3), nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="trips")
