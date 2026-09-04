from fastapi import FastAPI
from app.database import Base, engine
from app.models import customer
from app.routers import customer

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customer.router)


@app.get("/")
def read_root():
    return {"mesaj": "Veresiye API çalışıyor"}