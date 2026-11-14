"""Small in-memory inventory. No database or HTTP interface exists."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    quantity: int


class Inventory:
    def __init__(self):
        self._items = {}

    def add_item(self, item: Item) -> None:
        if item.sku in self._items:
            raise KeyError(f"duplicate sku: {item.sku}")
        if item.quantity <= 0:
            raise ValueError("quantity must be positive")
        self._items[item.sku] = item

    def get(self, sku: str) -> Item:
        return self._items[sku]
