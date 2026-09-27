"""
PyTest suite for product search + add to cart
(automationexercise.com/products).

Run:
    pytest tests_pytest/test_product_search_pytest.py -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from pages.product_search_page import ProductSearchPage
from utils.csv_reader import read_csv

SEARCH_ROWS = read_csv("test_data/search_data.csv")


@pytest.mark.parametrize(
    "row", SEARCH_ROWS, ids=[r["description"].replace(" ", "_") for r in SEARCH_ROWS]
)
def test_search_returns_expected_results(logged_in_driver, row):
    search_page = ProductSearchPage(logged_in_driver)
    search_page.load().search(row["search_term"])

    if row["expect_results"] == "true":
        assert search_page.get_product_card_count() > 0, row["description"]
    else:
        assert search_page.has_no_results_message(), row["description"]


def test_add_to_cart_updates_badge(logged_in_driver):
    search_page = ProductSearchPage(logged_in_driver)
    search_page.load().search("Blue Top")
    search_page.add_first_result_to_cart()
    assert search_page.cart_contains("Blue Top")
