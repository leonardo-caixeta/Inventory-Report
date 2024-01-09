from typing import List, Type

import pytest

from inventory_report.inventory import Inventory
from inventory_report.product import Product
from inventory_report.reports import CompleteReport, Report, SimpleReport
from tests.conftest import (
    CLOSEST_DATE,
    COMPANY_WITH_THE_LARGEST_INVENTORY,
    OLDEST_DATE,
)


@pytest.mark.parametrize(
    "report_class",
    [
        pytest.param(SimpleReport, marks=pytest.mark.dependency),
        pytest.param(CompleteReport, marks=pytest.mark.dependency),
    ],
)
def test_generate_returns_correct_oldest_date(
    inventories: List[Inventory], report_class: Type[Report]
) -> None:
    for inventory in inventories:
        report = report_class()
        report.add_inventory(inventory)
        result = report.generate()
        assert f"Oldest manufacturing date: {OLDEST_DATE}" in result


@pytest.mark.parametrize(
    "report_class",
    [
        pytest.param(SimpleReport, marks=pytest.mark.dependency),
        pytest.param(CompleteReport, marks=pytest.mark.dependency),
    ],
)
def test_generate_returns_correct_closest_expiration_date(
    inventories: List[Inventory], report_class: Type[Report]
) -> None:
    for inventory in inventories:
        report = report_class()
        report.add_inventory(inventory)
        result = report.generate()
        assert f"Closest expiration date: {CLOSEST_DATE}" in result


@pytest.mark.dependency
def test_generate_returns_correct_company_with_the_largest_inventory(
    inventories: List[Inventory],
) -> None:
    for inventory in inventories:
        report = SimpleReport()
        report.add_inventory(inventory)
        result = report.generate()
        assert (
            "Company with the largest inventory: "
            f"{COMPANY_WITH_THE_LARGEST_INVENTORY}" in result
        )


@pytest.mark.dependency
def test_generate_returns_correct_output(products: List[Product]) -> None:
    inventory = Inventory(products)
    report = SimpleReport()
    report.add_inventory(inventory)
    result = report.generate()
    assert f"Oldest manufacturing date: {OLDEST_DATE}" in result
    assert f"Closest expiration date: {CLOSEST_DATE}" in result
    assert (
        f"Company with the largest inventory: "
        f"{COMPANY_WITH_THE_LARGEST_INVENTORY}"
    ) in result


# Testes do requisito 7
@pytest.mark.dependency(
    depends=[
        "test_generate_returns_correct_oldest_date[SimpleReport]",
        "test_generate_returns_correct_closest_expiration_date[SimpleReport]",
        "test_generate_returns_correct_company_with_the_largest_inventory",
        "test_generate_returns_correct_output",
    ]
)
def test_simple_report() -> None:
    pass


@pytest.mark.dependency
def test_generate_returns_correct_stocked_products_by_company(
    inventories: List[Inventory],
    products: List[Product],
) -> None:
    for inventory in inventories:
        report = CompleteReport()
        report.add_inventory(inventory)
        result = report.generate()

        expected = [
            "Stocked products by company:\n",
            f"- {COMPANY_WITH_THE_LARGEST_INVENTORY}: 3\n",
            f"- {products[-2].company_name}: 1\n",
            f"- {products[-1].company_name}: 1\n",
        ]
        for expect in expected:
            assert expect in result


@pytest.mark.dependency
def test_generate_returns_correct_output_complete_report(
    inventories: List[Inventory],
    products: List[Product],
) -> None:
    for inventory in inventories:
        report = CompleteReport()
        report.add_inventory(inventory)
        result = report.generate()
        expect_start = (
            f"Oldest manufacturing date: {OLDEST_DATE}\n"
            f"Closest expiration date: {CLOSEST_DATE}\n"
            "Company with the largest inventory: "
            f"{COMPANY_WITH_THE_LARGEST_INVENTORY}\n"
            "Stocked products by company:\n",
        )
        expected = [
            f"- {COMPANY_WITH_THE_LARGEST_INVENTORY}: 3\n",
            f"- {products[-2].company_name}: 1\n",
            f"- {products[-1].company_name}: 1\n",
        ]
        assert result.startswith(expect_start)
        for expect in expected:
            assert expect in result


# Teste do requisito 9
@pytest.mark.dependency(
    depends=[
        "test_simple_report",
        "test_generate_returns_correct_oldest_date[CompleteReport]",
        "test_generate_returns_correct_closest_expiration_date"
        "[CompleteReport]",
        "test_generate_returns_correct_stocked_products_by_company",
        "test_generate_returns_correct_output_complete_report",
    ]
)
def test_complete_report() -> None:
    pass
