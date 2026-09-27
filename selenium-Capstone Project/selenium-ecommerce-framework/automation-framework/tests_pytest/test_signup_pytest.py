"""
PyTest suite for account registration (automationexercise.com/signup).

Registers a throwaway account, verifies login state, logs out, logs
back in, then deletes the account — the full user lifecycle.

Run:
    pytest tests_pytest/test_signup_pytest.py -v
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.signup_page import SignupPage


def test_signup_login_logout_delete_lifecycle(driver):
    stamp = int(time.time() * 1000) % 10000000000
    name = f"Lifecycle{stamp}"
    email = f"lifecycle{stamp}@example.com"
    password = "Test@1234"

    signup_page = SignupPage(driver)
    signup_page.start_signup(name, email)
    signup_page.fill_account_info(password)
    signup_page.continue_as_logged_in()

    login_page = LoginPage(driver)
    assert login_page.is_login_successful(), "Newly registered user should be logged in"

    login_page.logout()
    login_page.load().login(email, password)
    assert login_page.is_login_successful(), "Re-login with new credentials should work"

    signup_page.delete_account()
