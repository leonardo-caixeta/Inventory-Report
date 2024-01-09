from typing import TYPE_CHECKING

import pytest
from mypy import api as mypy_api

from inventory_report.inventory import Inventory
from inventory_report.reports import Report

from tests.conftest import remove_mypy_cache


class MockReport:
    def add_inventory(self, inventory: Inventory) -> None:
        self.inventory = inventory

    def generate(self) -> str:
        return ""


def func_that_uses_report_protocol(rep: Report) -> None:
    rep.generate().splitlines()


if TYPE_CHECKING:
    report = MockReport()
    report.add_inventory(Inventory())
    func_that_uses_report_protocol(report)


@pytest.mark.dependency
def test_generate_receive_self() -> None:
    report_generate_params = Report.generate.__code__.co_varnames
    assert "self" in report_generate_params
    assert len(report_generate_params) == 1


@pytest.mark.dependency
def test_generate_return_str() -> None:
    assert Report.generate.__annotations__["return"] == str


@pytest.mark.dependency
def test_add_inventory_receive_self_and_inventory() -> None:
    report_add_inventory_params = Report.add_inventory.__code__.co_varnames
    assert "self" in report_add_inventory_params
    assert "inventory" in report_add_inventory_params
    assert len(report_add_inventory_params) == 2


@pytest.mark.dependency
def test_add_inventory_return_none() -> None:
    assert Report.add_inventory.__annotations__["return"] is None


# Teste do requisito 6
@pytest.mark.dependency(
    depends=[
        "test_generate_receive_self",
        "test_generate_return_str",
        "test_add_inventory_receive_self_and_inventory",
        "test_add_inventory_return_none",
    ]
)
def test_report_final() -> None:
    remove_mypy_cache()

    # Run mypy programmatically on the test file
    # If the Report protocol is implemented incorrectly, ideally mypy should
    # raise a typing error, returning an error code.
    # TODO: Test with inspect instead of mypy
    _stdout, _stderr, exit_code = mypy_api.run([__file__])
    assert not exit_code, "Garanta que a classe Report seja um protocolo"

    remove_mypy_cache()
