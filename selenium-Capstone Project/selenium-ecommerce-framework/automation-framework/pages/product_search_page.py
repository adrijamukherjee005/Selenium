"""
Page Object for product search / listing
(https://automationexercise.com/products).

Search submits to /products?search=<term>. Adding to cart pops the
#cartModal dialog; cart contents are asserted on /view_cart.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from config.config_reader import ConfigReader


class ProductSearchPage(BasePage):
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".single-products")
    # .productinfo is the always-visible card body (overlay duplicates names on hover).
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".productinfo a.add-to-cart")
    CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "#cartModal .close-modal")
    CART_TABLE_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    CART_DESCRIPTIONS = (By.CSS_SELECTOR, "#cart_info_table .cart_description")

    def load(self):
        self.open(ConfigReader.base_url() + "/products")
        return self

    def search(self, term):
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        return self

    def get_product_names(self):
        return [el.text.strip() for el in self.find_all(self.PRODUCT_NAMES)]

    def get_product_card_count(self):
        try:
            return len(self.find_all(self.PRODUCT_CARDS))
        except Exception:
            return 0

    def has_no_results_message(self):
        # The site renders no cards (and no dedicated empty-state banner)
        # when nothing matches, so an empty grid is the signal.
        return self.get_product_card_count() == 0

    def add_first_result_to_cart(self):
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        button = buttons[0]
        # Ad iframes/overlays can intercept a native click; JS click is reliable.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
            button,
        )
        self._pause()
        # Dismiss the "Added!" confirmation modal.
        continue_button = self.find_clickable(self.CONTINUE_SHOPPING_BUTTON)
        try:
            continue_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", continue_button)
        WebDriverWait(self.driver, ConfigReader.explicit_wait()).until_not(
            lambda d: d.find_element(*self.CART_MODAL).is_displayed()
        )
        return self

    def open_cart(self):
        self.open(ConfigReader.base_url() + "/view_cart")
        return self

    def cart_contains(self, product_name):
        """True when /view_cart lists a product with this name."""
        self.open_cart()
        try:
            descriptions = self.find_all(self.CART_DESCRIPTIONS)
        except Exception:
            return False
        return any(
            product_name.lower() in el.text.lower() for el in descriptions
        )
