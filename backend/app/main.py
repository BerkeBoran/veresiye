from fastapi import FastAPI
from app.database import Base, engine
from app.models import customer, sale
from app.routers import customers, sales

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)
app.include_router(sales.router)

@app.get("/")
def read_root():
    return {"mesaj": "Veresiye API çalışıyor"}