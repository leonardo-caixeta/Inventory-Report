from inventory_report.product import Product


def test_product_report() -> None:
    product = Product(
        "420",
        "camomila",
        "Leo's Chás",
        "10/01/2024",
        "10/03/2024",
        "10203050420",
        "manter na embalagem",
    )

    assert "The product 420 - camomila" in product.__str__()
    assert "with serial number 10203050420" in product.__str__()
    assert "manufactured on 10/01/2024" in product.__str__()
    assert "by the company Leo's Chás" in product.__str__()
    assert "valid until 10/03/2024" in product.__str__()
    assert (
        "must be stored according to the following instructions: manter na embalagem" # NOQA
        in product.__str__()
    )
