import logging
from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, FastAPI
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel, BaseSettings


class DatabaseConfig(BaseSettings):
    host: str
    port: str
    name: str

    class Config:
        env_prefix = "DB_"
        case_sensitive = False


logger = logging.getLogger(__name__)


@lru_cache
def db_config() -> DatabaseConfig:
    # NOTE: If we don't specify any of the parameters, we get all of them from the environment
    return DatabaseConfig()  # type: ignore[missing-parameter]


async def database(
    # NOTE: Types are not going to match Depends as it is
    config: DatabaseConfig = Depends(db_config),  # type: ignore[assignment]
) -> AsyncIOMotorDatabase:
    """
    Grab yourself a database connection.
    """
    logger.info("Connecting database on host %r and port %r", config.host, config.port)
    client = AsyncIOMotorClient(f"mongodb://{config.host}:{config.port}")
    logger.info("Selecting database %r", config.name)
    return client[config.name]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


router = APIRouter(prefix="/api")


@router.get("")
async def read_root():
    return {"description": "An API built to interact with BIOS synchronized data."}


@router.get("/items")
async def list_items(database: AsyncIOMotorDatabase = Depends(database)):
    cursor = database.items.find()
    items = [{**i, "_id": str(i.get("_id"))} async for i in cursor]
    return items


@router.post("/items")
async def create_item(item: Item, database: AsyncIOMotorDatabase = Depends(database)):
    result = await database.items.insert_one(item.dict())
    return str(result.inserted_id)


def create_app():
    formatter = logging.Formatter(fmt=logging.BASIC_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    app = FastAPI()
    app.include_router(router)
    return app
