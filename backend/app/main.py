from fastapi import FastAPI
from app.database import Base, engine
from app.models import customer, sale, payment, shipment, daily_sale, vehicle, trip, vehicle_expense, partner_payment, purchase, supplier
from app.routers import customers, sales, payments, shipments, daily_sales, vehicles, trips, vehicle_expenses, partner_payments, suppliers, purchases
from app.core.middleware import register_middleware


app = FastAPI()

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

@app.get("/")
def read_root():
    return {"mesaj": "Veresiye API çalışıyor"}