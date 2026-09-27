"""
Base class every Page Object inherits from.

Centralises explicit waits and common interactions so individual page
classes stay declarative (locators + business methods only).
"""
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from config.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.explicit_wait())

    def _pause(self):
        delay = ConfigReader.slowmo()
        if delay > 0:
            time.sleep(delay)

    def open(self, url):
        self.driver.get(url)
        self._pause()

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.visibility_of_element_located(locator)) is not None
        except Exception:
            return False

    def click(self, locator):
        element = self.find_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Live-site hazard: a Google ad iframe can overlay the button.
            # A JS click dispatches directly to the element, bypassing the overlay.
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
                element,
            )
        self._pause()

    def type_text(self, locator, text, clear_first=True):
        # Wait for clickable (visible + enabled), not just present in DOM,
        # so hidden elements fail with a clear timeout instead of
        # ElementNotInteractableException on clear()/send_keys().
        element = self.find_clickable(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self._pause()

    def get_text(self, locator):
        return self.find(locator).text

    def title(self):
        return self.driver.title
