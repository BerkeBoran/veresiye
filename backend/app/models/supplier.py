from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    tax_number = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    address = Column(String, nullable=True)

    purchases = relationship("Purchase", back_populates="supplier")
    payments = relationship("Payment", back_populates="supplier")