from sqlalchemy import Column, Integer, ForeignKey, String, Float, func, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    product_name = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    vat_rate = Column(Float, nullable=False, default=0)

    subtotal = Column(Float, nullable=False)
    vat_amount = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="sales")
