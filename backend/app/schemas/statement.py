from pydantic import BaseModel

from app.schemas.customer import CustomerRead
from app.schemas.payment import PaymentRead
from app.schemas.sale import SaleRead
from decimal import Decimal

from app.schemas.shipment import ShipmentRead


class CustomerStatement(BaseModel):
    customer: CustomerRead
    total_sales: Decimal
    total_payments: Decimal
    total_shipments: Decimal
    balance: Decimal
    sales: list[SaleRead]
    shipments: list[ShipmentRead]
    payments: list[PaymentRead]