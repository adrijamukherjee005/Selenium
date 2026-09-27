"""
Shared PyTest fixtures and hooks for the whole suite.

- `driver` fixture: creates/quits a WebDriver per test.
- `ae_user` fixture (session): registers one throwaway account on
  automationexercise.com per run, yields its credentials, deletes it after.
- `logged_in_driver` fixture: driver already authenticated, landed on home.
- pytest_runtest_makereport + screenshot fixture: captures a screenshot on
  failure and (when pytest-html is installed) embeds it in the HTML report.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from config.config_reader import ConfigReader
from utils.driver_factory import DriverFactory
from utils.screenshot_utils import take_screenshot
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


@pytest.fixture
def driver():
    drv = DriverFactory.get_driver()
    yield drv
    # Optional watch mode: keep the browser open a while before quitting.
    keep_open = ConfigReader.keep_open_seconds()
    if keep_open > 0:
        time.sleep(keep_open)
    drv.quit()


@pytest.fixture(scope="session")
def ae_user():
    """Provision one throwaway account for the whole run."""
    drv = DriverFactory.get_driver()
    try:
        user = SignupPage(drv).register_unique_user()
        assert LoginPage(drv).is_login_successful(), "Fixture setup: signup failed"
        LoginPage(drv).logout()
        yield user
        # Cleanup: log back in and delete the account.
        LoginPage(drv).load().login(user["email"], user["password"])
        assert LoginPage(drv).is_login_successful(), "Fixture teardown: login failed"
        SignupPage(drv).delete_account()
    finally:
        drv.quit()


@pytest.fixture
def logged_in_driver(driver, ae_user):
    login_page = LoginPage(driver)
    login_page.load().login(ae_user["email"], ae_user["password"])
    assert login_page.is_login_successful(), "Fixture setup: demo login failed"
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver is not None:
            screenshot_path = take_screenshot(driver, item.name)
            if screenshot_path and hasattr(item.config, "_html"):
                # pytest-html: embed the screenshot as a relative link
                extra = getattr(report, "extra", [])
                try:
                    from pytest_html import extras
                    extra.append(extras.image(screenshot_path))
                    report.extra = extra
                except ImportError:
                    pass
