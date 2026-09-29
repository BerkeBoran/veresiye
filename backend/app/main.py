from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.scheduler import start_backup_scheduler, stop_backup_scheduler
from app.database import Base, engine
from app.models import customer, sale, payment, shipment, daily_sale, vehicle, trip, vehicle_expense, partner_payment, purchase, supplier
from app.routers import customers, sales, payments, shipments, daily_sales, vehicles, trips, vehicle_expenses, partner_payments, suppliers, purchases, backups
from app.core.middleware import register_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_backup_scheduler()
    yield
    stop_backup_scheduler()
app = FastAPI(lifespan=lifespan)

register_middleware(app)

app.include_router(customers.router)
app.include_router(sales.router)
app.include_router(payments.router)
app.include_router(shipments.router)
app.include_router(daily_sales.router)
app.include_router(vehicles.router)
app.include_router(trips.router)
app.include_router(vehicle_expenses.router)
app.include_router(partner_payments.router)
app.include_router(suppliers.router)
app.include_router(purchases.router)
app.include_router(backups.router)

@app.get("/")
def read_root():
    return {"mesaj": "Veresiye API çalışıyor"}