"""
Screenshot-on-failure helper, shared by both the Unittest and PyTest suites.
"""
import os
import datetime

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")


def take_screenshot(driver, test_name):
    """Save a screenshot named <test_name>_<timestamp>.png and return its path."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in test_name)
    filepath = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{timestamp}.png")
    try:
        driver.save_screenshot(filepath)
        return filepath
    except Exception as exc:  # pragma: no cover - best-effort capture
        print(f"[screenshot_utils] Failed to capture screenshot: {exc}")
        return None
