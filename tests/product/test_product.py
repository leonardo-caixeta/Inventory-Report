from inventory_report.product import Product


def test_create_product() -> None:
    product = Product(
        '420',
        'camomila',
        "Leo's Chás",
        '10/01/2024',
        '10/03/2024',
        '10203050420',
        'manter na embalagem'
    )
    assert product.id == "420"
    assert product.product_name == "camomila"
    assert product.company_name == "Leo's Chás"
    assert product.manufacturing_date == "10/01/2024"
    assert product.expiration_date == "10/03/2024"
    assert product.serial_number == "10203050420"
    assert product.storage_instructions == "manter na embalagem"
