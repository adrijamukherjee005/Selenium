"""
Unittest suite for the Login functionality (automationexercise.com/login).

One throwaway account is registered in setUpClass and deleted in
tearDownClass, so no manual test data is needed.

Run directly:
    python -m unittest discover -s tests_unittest -v
"""
import sys
import os
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import ConfigReader
from utils.driver_factory import DriverFactory
from utils.screenshot_utils import take_screenshot
from utils.csv_reader import read_csv
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


class TestLoginUnittest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        drv = DriverFactory.get_driver()
        try:
            cls.user = SignupPage(drv).register_unique_user()
            assert LoginPage(drv).is_login_successful(), "Setup: signup failed"
            LoginPage(drv).logout()
        finally:
            drv.quit()

    @classmethod
    def tearDownClass(cls):
        drv = DriverFactory.get_driver()
        try:
            login_page = LoginPage(drv)
            login_page.load().login(cls.user["email"], cls.user["password"])
            assert login_page.is_login_successful(), "Teardown: login failed"
            SignupPage(drv).delete_account()
        finally:
            drv.quit()

    def setUp(self):
        self.driver = DriverFactory.get_driver()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        # Screenshot on failure: unittest exposes failures/errors via _outcome
        outcome = getattr(self, "_outcome", None)
        had_failure = False
        if outcome is not None:
            result = outcome.result
            had_failure = any(self is t[0] for t in result.failures + result.errors)
        if had_failure:
            take_screenshot(self.driver, self._testMethodName)
        keep_open = ConfigReader.keep_open_seconds()
        if keep_open > 0:
            time.sleep(keep_open)
        self.driver.quit()

    def test_valid_login_shows_shop_section(self):
        self.login_page.load().login(self.user["email"], self.user["password"])
        self.assertTrue(self.login_page.is_login_successful(), "Logout link should be visible after valid login")

    def test_invalid_login_shows_error(self):
        self.login_page.load().login(self.user["email"], "WrongPassword1")
        error = self.login_page.get_error_message()
        self.assertIsNotNone(error, "An error message should be shown for invalid credentials")

    def test_login_data_driven_from_csv(self):
        """Data-driven variant: iterates login_data.csv within a single test."""
        rows = read_csv("test_data/login_data.csv")
        for row in rows:
            with self.subTest(description=row["description"]):
                self.login_page.load().login(row["email"], row["password"])
                if row["expected_result"] == "success":
                    self.assertTrue(self.login_page.is_login_successful(), row["description"])
                else:
                    self.assertFalse(self.login_page.is_login_successful(), row["description"])


if __name__ == "__main__":
    unittest.main()
