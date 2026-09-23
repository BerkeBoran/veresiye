from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Numeric, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    payment_date = Column(Date, nullable=True)
    direction = Column(String, nullable=True, server_default="in")
    payment_type = Column(String, nullable=True, server_default="cash")
    bank_name = Column(String, nullable=True)
    cheque_no = Column(String, nullable=True)
    cheque_due_date = Column(Date, nullable=True)

    customer = relationship("Customer", back_populates="payments")