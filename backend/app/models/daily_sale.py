from sqlalchemy import Column, Integer, Date, String, Numeric, Boolean, func, DateTime

from app.database import Base


class DailySale(Base):
    __tablename__ = "daily_sales"

    id = Column(Integer, primary_key=True, index=True)

    sale_date = Column(Date, nullable=False)
    place_of_shipment = Column(String, nullable=True)
    number_plate = Column(String, nullable=True)
    product_name = Column(String, nullable=True)

    kg = Column(Numeric(10,3), nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    vat_exempt = Column(Boolean, nullable=False, server_default="0")
    vat_rate = Column(Numeric(5,2), nullable=False, server_default="20")

    subtotal = Column(Numeric(12,2), nullable=False)
    vat_amount = Column(Numeric(12,2), nullable=False)
    total = Column(Numeric(12,2), nullable=False)

    created_at = Column(DateTime, nullable=True, server_default=func.now())