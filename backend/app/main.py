from fastapi import FastAPI
from app.database import Base, engine
from app.models import customer, sale, payment, shipment, daily_sale, vehicle, trip, vehicle_expense
from app.routers import customers, sales, payments, shipments, daily_sales, vehicles, trips, vehicle_expenses
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

@app.get("/")
def read_root():
    return {"mesaj": "Veresiye API çalışıyor"}