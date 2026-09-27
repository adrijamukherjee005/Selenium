from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config_reader import ConfigReader


class LoginPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    # Rendered only after a failed login POST ("Your email or password is incorrect!").
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-form p")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    LOGGED_IN_AS = (By.PARTIAL_LINK_TEXT, "Logged in as")

    def load(self):
        self.open(ConfigReader.base_url() + "/login")
        return self

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def logout(self):
        self.click(self.LOGOUT_LINK)
        return self

    def get_error_message(self):
        if self.is_visible(self.ERROR_MESSAGE, timeout=10):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_successful(self):
        return self.is_visible(self.LOGOUT_LINK, timeout=10)
