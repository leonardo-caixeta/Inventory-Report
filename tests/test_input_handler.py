# flake8: noqa

import pytest

from inventory_report.cli import input_handler
from tests.conftest import (
    CLOSEST_DATE,
    COMPANY_WITH_THE_LARGEST_INVENTORY,
    OLDEST_DATE,
)


@pytest.mark.parametrize(
    "report_type",
    [
        pytest.param("simple", marks=pytest.mark.dependency),
        pytest.param("complete", marks=pytest.mark.dependency),
    ],
)
def test_process_report_returns_correct_oldest_date(report_type: str) -> None:
    result = input_handler.process_report_request(
        ["inventory_report/data/inventory.csv"], report_type
    )
    assert f"Oldest manufacturing date: {OLDEST_DATE}" in result


@pytest.mark.parametrize(
    "report_type",
    [
        pytest.param("simple", marks=pytest.mark.dependency),
        pytest.param("complete", marks=pytest.mark.dependency),
    ],
)
def test_process_report_returns_correct_closest_expiration_date(
    report_type: str,
) -> None:
    result = input_handler.process_report_request(
        ["inventory_report/data/inventory.csv"], report_type
    )
    assert f"Closest expiration date: {CLOSEST_DATE}" in result


@pytest.mark.parametrize(
    "report_type",
    [
        pytest.param("simple", marks=pytest.mark.dependency),
        pytest.param("complete", marks=pytest.mark.dependency),
    ],
)
def test_process_report_returns_correct_company_with_largest_inventory(
    report_type: str,
) -> None:
    result = input_handler.process_report_request(
        ["inventory_report/data/inventory.csv"], report_type
    )
    assert (
        f"Company with the largest inventory: {COMPANY_WITH_THE_LARGEST_INVENTORY}"
        in result
    )


def test_process_report_should_raise_error_with_invalid_report_type() -> None:
    with pytest.raises(ValueError, match="Report type is invalid."):
        input_handler.process_report_request(
            ["inventory_report/data/inventory.csv"], "invalid"
        )


@pytest.mark.parametrize(
    "report_type",
    [
        pytest.param("simple", marks=pytest.mark.dependency),
        pytest.param("complete", marks=pytest.mark.dependency),
    ],
)
def test_process_report_should_ignore_unsuported_inventory_files(
    report_type: str,
) -> None:
    first_result = input_handler.process_report_request(
        ["inventory_report/data/inventory.csv"], report_type
    )

    second_result = input_handler.process_report_request(
        [
            "inventory_report/data/inventory.csv",
            "inventory_report/data/inventory.txt",
        ],
        report_type,
    )

    assert first_result == second_result


def test_process_report_should_use_all_supported_files_available(
    products,
) -> None:
    result = input_handler.process_report_request(
        [
            "inventory_report/data/inventory.csv",
            "inventory_report/data/inventory.json",
        ],
        "complete",
    )

    expected = (
        "Stocked products by company:\n"
        f"- {COMPANY_WITH_THE_LARGEST_INVENTORY}: 6\n"
        f"- {products[-2].company_name}: 2\n"
        f"- {products[-1].company_name}: 2\n"
    )

    assert expected in result


# Testes do requisito 10
@pytest.mark.dependency(
    depends=[
        "test_process_report_returns_correct_oldest_date[simple]",
        "test_process_report_returns_correct_oldest_date[complete]",
        "test_process_report_returns_correct_closest_expiration_date[simple]",
        "test_process_report_returns_correct_closest_expiration_date[complete]",
        "test_process_report_returns_correct_company_with_largest_inventory[simple]",
        "test_process_report_returns_correct_company_with_largest_inventory[complete]",
        "test_process_report_should_ignore_unsuported_inventory_files[simple]",
        "test_process_report_should_ignore_unsuported_inventory_files[complete]",
        "test_process_report_should_raise_error_with_invalid_report_type",
        "test_process_report_should_use_all_supported_files_available",
    ],
)
def test_process_report_final() -> None:
    pass
