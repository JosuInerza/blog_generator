from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter()
service = ItemService()


@router.post("/", response_model=Item, status_code=201)
def create_item(data: ItemCreate):
    return service.create_item(data)


@router.get("/", response_model=List[Item])
def list_items():
    return service.list_items()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(404, "Item not found")
    return
