import os
from typing import Optional

from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel

print(os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("SERVER_DB_NAME"))

db_client = MongoClient(os.getenv("DB_HOST"), int(os.getenv("DB_PORT")))
db_instance = db_client[os.getenv("SERVER_DB_NAME")]
app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
def read_root():
    return {"description": "An API built to interact with BIOS synchronized data."}

@app.post("/test/item")
def read_root(item: Item):
    result = db_instance.items.insert_one(item.dict())
    return str(result.inserted_id)

@app.get("/test/items")
def read_root():
    items = [{**i, "_id": str(i.get("_id"))} for i in db_instance.items.find()]
    print(items)
    return items