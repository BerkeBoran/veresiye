from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

from app.core.config import FRONTEND_DIR
from app.core.migrations import upgrade_database
from app.core.scheduler import start_backup_scheduler, stop_backup_scheduler
from app.models import customer, sale, payment, shipment, daily_sale, vehicle, trip, vehicle_expense, partner_payment, purchase, supplier
from app.routers import customers, sales, payments, shipments, daily_sales, vehicles, trips, vehicle_expenses, partner_payments, suppliers, purchases, backups
from app.core.middleware import register_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    upgrade_database()
    start_backup_scheduler()
    yield
    stop_backup_scheduler()
app = FastAPI(lifespan=lifespan)

register_middleware(app)

API_ROUTERS = [
    customers.router,
    sales.router,
    payments.router,
    shipments.router,
    daily_sales.router,
    vehicles.router,
    trips.router,
    vehicle_expenses.router,
    partner_payments.router,
    suppliers.router,
    purchases.router,
    backups.router,
]
for router in API_ROUTERS:
    app.include_router(router, prefix="/api")

@app.get("/{full_path:path}", include_in_schema=False)
def frontend(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Böyle bir API adresi yok.")

    file = (FRONTEND_DIR / full_path).resolve()
    if full_path and file.is_file() and file.is_relative_to(FRONTEND_DIR.resolve()):
        return FileResponse(file)

    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Frontend derlenmemiş")
    return FileResponse(index)