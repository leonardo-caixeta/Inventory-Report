import csv
import json
from typing import Dict, Type
from abc import ABC, abstractmethod

from inventory_report.product import Product


class Importer(ABC):
    def __init__(self, path: str) -> None:
        self.path = path

    @abstractmethod
    def import_data(self) -> list[Product]:
        pass


class JsonImporter(Importer):
    def import_data(self) -> list[Product]:
        products = []
        with open(self.path) as file:
            data = json.load(file)
            for d in data:
                product = Product(
                    d["id"],
                    d["product_name"],
                    d["company_name"],
                    d["manufacturing_date"],
                    d["expiration_date"],
                    d["serial_number"],
                    d["storage_instructions"],
                )
                products.append(product)

        return products


class CsvImporter(Importer):
    def import_data(self) -> list[Product]:
        products = []
        with open(self.path, 'r', newline="") as file:
            data = csv.DictReader(file)
            for d in data:
                product = Product(
                    d["id"],
                    d["product_name"],
                    d["company_name"],
                    d["manufacturing_date"],
                    d["expiration_date"],
                    d["serial_number"],
                    d["storage_instructions"],
                )
                products.append(product)

        return products


# Não altere a variável abaixo

IMPORTERS: Dict[str, Type[Importer]] = {
    "json": JsonImporter,
    "csv": CsvImporter,
}
