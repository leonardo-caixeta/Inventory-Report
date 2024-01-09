from abc import ABC

import pytest

from inventory_report.importers import CsvImporter, Importer, JsonImporter
from inventory_report.product import Product
from tests.conftest import (
    generate_data_using_seed,
    mock_url,
    _prepare_product_data,
)


@pytest.mark.dependency
def test_importer_is_abstract() -> None:
    assert issubclass(Importer, ABC)


@pytest.mark.dependency
def test_importer_init_is_not_abstract() -> None:
    with pytest.raises(
        AttributeError,
        match="'function' object has no attribute '__isabstractmethod__'",
    ):
        Importer.__init__.__isabstractmethod__  # type:ignore


@pytest.mark.dependency
def test_importer_init_receive_self_and_path() -> None:
    importer_init_params = Importer.__init__.__code__.co_varnames
    assert "self" in importer_init_params
    assert "path" in importer_init_params
    assert len(importer_init_params) == 2


@pytest.mark.dependency
def test_importer_init_path_is_str() -> None:
    assert Importer.__init__.__annotations__["path"] == str


@pytest.mark.dependency
def test_importer_import_data_is_abstractmethod() -> None:
    assert Importer.import_data.__isabstractmethod__  # type:ignore


@pytest.mark.dependency
def test_importer_import_data_receive_self() -> None:
    importer_import_data_params = Importer.import_data.__code__.co_varnames
    assert "self" in importer_import_data_params
    assert len(importer_import_data_params) == 1


@pytest.mark.dependency
def test_importer_import_data_return_list_of_products() -> None:
    assert (
        str(Importer.import_data.__annotations__["return"])
        .lower()
        .replace("typing.", "")
        == "list[inventory_report.product.product]"
    )


# Teste do requisito 3
@pytest.mark.dependency(
    depends=[
        "test_importer_is_abstract",
        "test_importer_init_is_not_abstract",
        "test_importer_init_receive_self_and_path",
        "test_importer_init_path_is_str",
        "test_importer_import_data_is_abstractmethod",
        "test_importer_import_data_receive_self",
        "test_importer_import_data_return_list_of_products",
    ]
)
def test_importer_final() -> None:
    pass


@pytest.mark.dependency
def test_json_importer_extends_importer() -> None:
    assert issubclass(JsonImporter, Importer)


PRODUCTS = [
    Product(**product)
    for product in _prepare_product_data(
        generate_data_using_seed(
            mock_url,
            5,
        )
    )
]


# Teste do requisito 4
@pytest.mark.dependency(depends=["test_json_importer_extends_importer"])
def test_validate_json_importer() -> None:
    report = JsonImporter("inventory_report/data/inventory.json").import_data()
    assert report == PRODUCTS


@pytest.mark.dependency
def test_csv_importer_extends_importer() -> None:
    assert issubclass(CsvImporter, Importer)


# Teste do requisito 8
@pytest.mark.dependency(depends=["test_csv_importer_extends_importer"])
def test_validate_csv_importer() -> None:
    report = CsvImporter("inventory_report/data/inventory.csv").import_data()
    assert report == PRODUCTS
