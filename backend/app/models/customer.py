from sqlalchemy import Column, String, Integer

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    tax_number = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    address = Column(String, nullable=True)
