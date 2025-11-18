from typing import List, Optional
from app.schemas import ItemCreate, Item


class ItemService:
    def __init__(self):
        self._items = {}
        self._next_id = 1

    def create_item(self, data: ItemCreate) -> Item:
        item = Item(id=self._next_id, **data.dict())
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def list_items(self) -> List[Item]:
        return list(self._items.values())

    def get_item(self, item_id: int) -> Optional[Item]:
        return self._items.get(item_id)

    def delete_item(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None
