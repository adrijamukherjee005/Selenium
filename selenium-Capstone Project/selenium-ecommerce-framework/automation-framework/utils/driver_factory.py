"""
Factory for creating configured WebDriver instances.

Kept separate from tests/pages so the driver-creation logic (browser choice,
headless flag, window size, timeouts) lives in exactly one place.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config_reader import ConfigReader


class DriverFactory:

    @staticmethod
    def get_driver(browser=None, headless=None):
        browser = (browser or ConfigReader.browser()).lower()
        headless = ConfigReader.headless() if headless is None else headless

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            # Silence Chrome's own stderr noise (GPU, updater, GCM logs)
            # so the console shows only test output.
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver = webdriver.Firefox(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(ConfigReader.implicit_wait())
        driver.set_page_load_timeout(ConfigReader.page_load_timeout())
        return driver
