
from sqlalchemy import Column, Integer, ForeignKey, String, func, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    note = Column(String, nullable=True)
    document_no = Column(String, nullable=True)
    vat_exempt = Column(Boolean, nullable=False, default=False, server_default="0")

    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    total = Column(Numeric(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    transport = Column(Boolean, nullable=True, server_default="0")
    transport_price = Column(Numeric(12,2), nullable=True)
    transport_vat_rate = Column(Numeric(5,2), nullable=False, server_default="20")
    transport_tevkifat = Column(Numeric(12,2), nullable=False, server_default="0")
    transport_vat_amount = Column(Numeric(12,2), nullable=False, server_default="0")
    transport_total = Column(Numeric(12,2), nullable=False, server_default="0")

    customer = relationship("Customer", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)

    product_name = Column(String, nullable=False)
    quantity_kg = Column(Numeric(10,3), nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    vat_rate = Column(Numeric(5,2), nullable=False, default=0)

    line_subtotal = Column(Numeric(12,2), nullable=False)
    line_total = Column(Numeric(12,2), nullable=False)
    line_vat = Column(Numeric(12,2), nullable=False)

    sale = relationship("Sale", back_populates="items")