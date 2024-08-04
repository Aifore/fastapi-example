import logging

from fastapi import APIRouter

from core.models.pydantic import Item
from core.models.tortoise import Item as TItem

router = APIRouter()


@router.get("/666")
async def read_root():
    logging.error("Hello World")
    return {"Hello": "World"}


@router.post("/", description="Create a new item")
async def post(item: Item):
    i = await TItem.create(**item.model_dump())
    await i.save()
    return {"response": "Successfully created new one"}


@router.get("/", description="Get all items")
async def get() -> list[Item]:
    items = await TItem.all()
    return items
