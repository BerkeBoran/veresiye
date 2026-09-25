from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    place_of_shipment = Column(String, nullable=True)
    shipment_date = Column(String, nullable=True)
    number_plate = Column(String, nullable=True)

    vat_exempt = Column(Boolean, nullable=False, default=False, server_default="0")
    unit_price = Column(Numeric(12,2), nullable=False)
    kg = Column(Numeric(10,3), nullable=False)
    vat_rate = Column(Numeric(5,2), nullable=False, server_default="20")

    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    tevkifat = Column(Numeric(12,2), nullable=False)
    total = Column(Numeric(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="shipments")


