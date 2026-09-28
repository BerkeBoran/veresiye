from sqlalchemy import Column, Integer, Date, Numeric, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class PartnerPayment(Base):
    __tablename__ = "partner_payments"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="partner_payments")