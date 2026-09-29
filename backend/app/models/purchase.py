from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    notes = Column(String, nullable=True)
    document_no = Column(String, nullable=True)
    vat_exempt = Column(Boolean, nullable=False, default=False, server_default="0")

    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    total = Column(Numeric(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    due_date = Column(Date, nullable=True)
    purchase_date = Column(Date, nullable=True)

    supplier = relationship("Supplier", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)

    product_name = Column(String, nullable=False)
    quantity_kg = Column(Numeric(10,3), nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    vat_rate = Column(Numeric(5,2), nullable=False, default=0)

    line_subtotal = Column(Numeric(12,2), nullable=False)
    line_total = Column(Numeric(12,2), nullable=False)
    line_vat = Column(Numeric(12,2), nullable=False)

    purchase = relationship("Purchase", back_populates="items")