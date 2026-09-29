from pydantic import BaseModel

from app.schemas.customer import CustomerRead
from app.schemas.payment import PaymentRead
from app.schemas.purchase import PurchaseRead
from app.schemas.sale import SaleRead
from decimal import Decimal

from app.schemas.shipment import ShipmentRead
from app.schemas.supplier import SupplierRead


class CustomerStatement(BaseModel):
    customer: CustomerRead
    total_sales: Decimal
    total_payments: Decimal
    total_shipments: Decimal
    balance: Decimal
    sales: list[SaleRead]
    shipments: list[ShipmentRead]
    payments: list[PaymentRead]


class SupplierStatement(BaseModel):
    supplier: SupplierRead
    total_purchases: Decimal
    total_payments: Decimal
    balance: Decimal
    purchases: list[PurchaseRead]
    payments: list[PaymentRead]