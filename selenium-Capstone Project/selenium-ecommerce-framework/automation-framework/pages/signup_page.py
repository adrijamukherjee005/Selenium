"""
Page Object for account registration and deletion
(https://automationexercise.com/login -> /signup -> /delete_account).

Used by fixtures to provision a throwaway user per test run, so the
login suite has valid credentials without any manual setup.
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from config.config_reader import ConfigReader


class SignupPage(BasePage):
    # Step 1 — "New User Signup!" form on /login
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    SIGNUP_ERROR = (By.CSS_SELECTOR, ".signup-form p")

    # Step 2 — "Enter Account Information" form on /signup
    TITLE_MR = (By.ID, "id_gender1")
    PASSWORD = (By.CSS_SELECTOR, "input[data-qa='password']")
    DAYS = (By.CSS_SELECTOR, "select[data-qa='days']")
    MONTHS = (By.CSS_SELECTOR, "select[data-qa='months']")
    YEARS = (By.CSS_SELECTOR, "select[data-qa='years']")
    FIRST_NAME = (By.CSS_SELECTOR, "input[data-qa='first_name']")
    LAST_NAME = (By.CSS_SELECTOR, "input[data-qa='last_name']")
    COMPANY = (By.CSS_SELECTOR, "input[data-qa='company']")
    ADDRESS = (By.CSS_SELECTOR, "input[data-qa='address']")
    ADDRESS2 = (By.CSS_SELECTOR, "input[data-qa='address2']")
    COUNTRY = (By.CSS_SELECTOR, "select[data-qa='country']")
    STATE = (By.CSS_SELECTOR, "input[data-qa='state']")
    CITY = (By.CSS_SELECTOR, "input[data-qa='city']")
    ZIPCODE = (By.CSS_SELECTOR, "input[data-qa='zipcode']")
    MOBILE = (By.CSS_SELECTOR, "input[data-qa='mobile_number']")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    # Confirmation pages ("Account Created!" / "Account Deleted!")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def start_signup(self, name, email):
        """Submit step 1 on /login; lands on /signup."""
        self.open(ConfigReader.base_url() + "/login")
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)
        return self

    def _select_by_visible_text(self, locator, text):
        Select(self.find(locator)).select_by_visible_text(text)

    def fill_account_info(self, password="Test@1234"):
        """Fill step 2 on /signup and submit; lands on 'Account Created!'."""
        self.click(self.TITLE_MR)
        self.type_text(self.PASSWORD, password)
        self._select_by_visible_text(self.DAYS, "10")
        self._select_by_visible_text(self.MONTHS, "May")
        self._select_by_visible_text(self.YEARS, "1995")
        self.type_text(self.FIRST_NAME, "Auto")
        self.type_text(self.LAST_NAME, "Tester")
        self.type_text(self.COMPANY, "QA Co")
        self.type_text(self.ADDRESS, "42 Test Street")
        self.type_text(self.ADDRESS2, "Suite 7")
        self._select_by_visible_text(self.COUNTRY, "India")
        self.type_text(self.STATE, "Karnataka")
        self.type_text(self.CITY, "Bengaluru")
        self.type_text(self.ZIPCODE, "560001")
        self.type_text(self.MOBILE, "9876543210")
        self.click(self.CREATE_ACCOUNT_BUTTON)
        return self

    def continue_as_logged_in(self):
        """Land on the home page logged in.

        The confirmation pages' Continue link triggers a fullscreen
        Google vignette ad instead of navigating, so go straight home:
        the session cookie is already set by the signup POST.
        """
        self.open(ConfigReader.base_url() + "/")
        return self

    def register_unique_user(self):
        """Full flow: signup -> account info -> continue. Returns dict."""
        stamp = int(time.time() * 1000) % 10000000000
        name = f"AutoTester{stamp}"
        email = f"autotester{stamp}@example.com"
        password = "Test@1234"
        self.start_signup(name, email)
        self.fill_account_info(password)
        self.continue_as_logged_in()
        return {"name": name, "email": email, "password": password}

    def delete_account(self):
        """Delete the currently logged-in account, then land on home.

        Deletion happens server-side on GET /delete_account; navigate
        home directly (see continue_as_logged_in for why we skip the
        Continue link).
        """
        self.open(ConfigReader.base_url() + "/delete_account")
        self.open(ConfigReader.base_url() + "/")
        return self
