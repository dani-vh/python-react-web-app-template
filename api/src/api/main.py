import os
import logging
from typing import Optional
from fastapi.params import Depends

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
from pydantic import BaseModel

logger = logging.getLogger()


async def database() -> AsyncIOMotorDatabase:
    """
    Grab yourself a database connection.
    """
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    logger.info("Connecting database on host %r and port %r", host, port)
    client = AsyncIOMotorClient(f"mongodb://{host}:{port}")
    logger.info("Selecting database %r", name)
    return client[name]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"description": "An API built to interact with BIOS synchronized data."}


@app.post("/test/item")
async def create_item(item: Item, database: AsyncIOMotorDatabase = Depends(database)):
    result = await database.items.insert_one(item.dict())
    return str(result.inserted_id)


@app.get("/test/items")
async def list_items(database: AsyncIOMotorDatabase = Depends(database)):
    cursor = database.items.find()
    items = [{**i, "_id": str(i.get("_id"))} async for i in cursor]
    return items
