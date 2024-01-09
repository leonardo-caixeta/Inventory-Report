import itertools
import configparser
import shutil
from datetime import date, timedelta
from typing import List, Dict
from git import Repo
import os
from csv import DictWriter
import json
import pytest
from faker import Faker

from inventory_report.inventory import Inventory
from inventory_report.product import Product

faker = Faker("pt-BR")

try:
    mock_email = (
        Repo.init(os.getcwd()).config_reader().get_value("user", "email")
    )

    mock_url = (
        Repo.init(os.getcwd())
        .config_reader()
        .get_value('remote "origin"', "url")
    )
except configparser.NoSectionError:
    mock_email = f"{faker.word()}@{faker.word()}.com"
    mock_url = f"https:/{faker.word()}.com"


OLDEST_DATE = date.today() - timedelta(days=366)
CLOSEST_DATE = date.today() + timedelta(days=1)
COMPANY_WITH_THE_LARGEST_INVENTORY = faker.company()


@pytest.fixture
def products() -> List[Product]:
    data = generate_data_using_seed(mock_url, 5)

    data = _prepare_product_data(data)

    return [Product(**product) for product in data]


@pytest.fixture
def inventories(products: List[Product]) -> List[Inventory]:
    return [
        Inventory(list(product))
        for product in itertools.permutations(products)
    ]


def remove_mypy_cache() -> None:
    try:
        shutil.rmtree(".mypy_cache")
    except (FileNotFoundError, OSError):
        pass


def generate_data_using_seed(seed: str, amount: int) -> List[Dict]:
    Faker.seed(seed)
    faker = Faker("pt_BR")

    return [
        {
            "id": str(faker.unique.random_int()),
            "product_name": faker.word(),
            "company_name": faker.company(),
            "manufacturing_date": str(faker.past_date(start_date="-365d")),
            "expiration_date": str(faker.future_date(end_date="+36500d")),
            "serial_number": faker.bothify(
                text="??## ???? #### #??? ?#?# ???? ??#?",
                letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            ),
            "storage_instructions": faker.paragraph(),
        }
        for _ in range(amount)
    ]


@pytest.fixture(scope="session", autouse=True)
def generate_files_inventory_data() -> None:
    data = generate_data_using_seed(
        mock_url,
        5,
    )

    data = _prepare_product_data(data)

    with open("inventory_report/data/inventory.csv", "w") as file:
        writer = DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    with open("inventory_report/data/inventory.json", "w") as fp:
        final = json.dumps(data, indent=2)
        fp.write(final)


def _prepare_product_data(data: List[Dict]) -> List[Dict]:
    data[-1]["manufacturing_date"] = str(OLDEST_DATE)
    data[-2]["expiration_date"] = str(CLOSEST_DATE)
    for i in range(3):
        data[i]["company_name"] = COMPANY_WITH_THE_LARGEST_INVENTORY
    return data


@pytest.fixture(scope="session", autouse=True)
def generate_files_test_mock_data() -> None:
    data: list[dict] = generate_data_using_seed(
        mock_email,
        100,
    )

    data[49].update(
        {
            "id": "999999",
            "company_name": "##".join(
                [data[::-1] for data in reversed(mock_email.split("@"))]
            ),
        }
    )

    if not os.path.exists("tests/mocks/inventory.csv"):
        with open("tests/mocks/inventory.csv", "w") as file:
            writer = DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    if not os.path.exists("tests/mocks/inventory.json"):
        with open("tests/mocks/inventory.json", "w") as fp:
            final = json.dumps(data, indent=2)
            fp.write(final)
