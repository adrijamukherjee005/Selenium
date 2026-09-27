"""
DEMO ONLY — intentionally failing test to showcase screenshot-on-failure.

It lives outside tests_pytest/ and tests_unittest/, so normal suite runs
never pick it up (pytest.ini testpaths = tests_pytest).

What it does: opens the home page WITHOUT logging in, then wrongly asserts
a logged-in user is shown. The assertion always fails, the conftest
pytest_runtest_makereport hook captures a screenshot into
reports/screenshots/, and pytest-html embeds it in reports/report.html.

Run ONLY this demo (overwrites reports/report.html — re-run the real suite
afterwards to restore a green report):
    python -m pytest demo_screenshot/ -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import ConfigReader
from pages.base_page import BasePage
from pages.login_page import LoginPage


def test_demo_failure_shows_screenshot(driver):
    page = BasePage(driver)
    page.open(ConfigReader.base_url() + "/")

    # Deliberately wrong: nobody logged in, so "Logged in as" is absent.
    assert LoginPage(driver).is_visible(LoginPage.LOGGED_IN_AS, timeout=5), (
        "DEMO FAILURE (on purpose): expected a logged-in user on a fresh visit"
    )
