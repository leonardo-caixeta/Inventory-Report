from typing import List

from inventory_report.product import Product


class Inventory:
    def __init__(self, data: List[Product] = None) -> None:
        self._data = data if data is not None else []

    @property
    def data(self):
        return self._data.copy()

    def add_data(self, data):
        self._data.extend(data)
