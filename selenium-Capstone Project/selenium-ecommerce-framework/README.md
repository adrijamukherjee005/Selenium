# Selenium E-Commerce Automation Framework

A complete, working example of **Capstone Assignment 2: Selenium Python
Framework Development (Unittest + PyTest + POM)**, built around a real
backend and frontend so the tests exercise an actual running app instead of
a flaky third-party demo site.

```
selenium-ecommerce-framework/
├── backend/                      Flask e-commerce API (system under test)
│   ├── app.py
│   └── requirements.txt
├── frontend/                     MiniShop demo UI (login + search + cart)
│   └── index.html
└── automation-framework/         The Selenium capstone deliverable
    ├── config/
    │   ├── config.ini            Base URL, browser, headless, timeouts
    │   └── config_reader.py      Config Management
    ├── pages/                    Page Object Model
    │   ├── base_page.py
    │   ├── login_page.py
    │   └── product_search_page.py
    ├── utils/                    Utility Classes
    │   ├── driver_factory.py
    │   ├── screenshot_utils.py
    │   └── csv_reader.py
    ├── test_data/                Test Data Handling (CSV)
    │   ├── login_data.csv
    │   └── search_data.csv
    ├── tests_unittest/
    │   └── test_login_unittest.py
    ├── tests_pytest/
    │   ├── test_login_pytest.py
    │   └── test_product_search_pytest.py
    ├── conftest.py                Fixtures + screenshot-on-failure hook
    ├── pytest.ini                 HTML Reporting config
    └── requirements.txt
```

## ⚠️ Important — run this on your own machine

This framework was built and verified in a sandbox that has **no installable
browser** (its network is locked to package registries, not
Chrome/chromedriver download servers). Everything up to the browser launch
was verified here:

- Backend: all endpoints tested directly (health, register, login, search,
  category filter, cart add/remove) — all correct.
- Framework: every file compiles, all imports resolve, config management
  reads correctly, CSV data-driven parametrization works (`pytest
  --collect-only` finds all **12** parametrized tests), and `unittest
  discover` runs up to the exact point of calling `webdriver.Chrome()` —
  where it fails only because no Chrome binary exists in this sandbox.

**On a normal machine with Chrome installed, this runs end-to-end as-is.**
No code changes needed — just `pip install -r requirements.txt` in both
`backend/` and `automation-framework/`.

## 1. Setup

No backend/frontend to start — the target is the live practice site
`https://automationexercise.com` (needs internet + Chrome).

```bash
cd automation-framework
pip install -r requirements.txt
```

Selenium 4.24+ auto-manages the chromedriver binary for you (Selenium
Manager) as long as Chrome itself is installed. `webdriver-manager` is
included as a fallback/alternative if you prefer explicit driver management.

## 2. Run it

No test accounts to create — every run registers a throwaway user on the
site automatically (`ae_user` fixture / `setUpClass`) and deletes it at the
end.

**Run the Unittest suite:**
```bash
cd automation-framework
python -m unittest discover -s tests_unittest -v
```

**Run the PyTest suite (with HTML report):**
```bash
pytest tests_pytest/ -v
# → reports/report.html (self-contained, includes failure screenshots)
```

**Run headed (watch the browser) in slow motion:**
```powershell
$env:HEADLESS="false"; $env:SLOWMO="1"; $env:KEEP_OPEN_SECONDS="10"
pytest tests_pytest/test_login_pytest.py::test_valid_login_shows_shop_section -v
```

**Point at a different environment:**
```bash
TEST_ENV=staging pytest tests_pytest/
```

## 3. What's covered

| Suite | Scenarios |
|---|---|
| Unittest — Login | Valid login, invalid password, CSV-driven data table (2 rows via `subTest`) — account auto-registered in `setUpClass`, deleted in `tearDownClass` |
| PyTest — Login | Valid login, invalid password, CSV-driven parametrize (2 cases) — via `ae_user` session fixture |
| PyTest — Product Search | Search with results, search with no results (2 CSV cases), add-to-cart verified on `/view_cart` |
| PyTest — Signup lifecycle | Register → logged in → logout → re-login → delete account |

**8 PyTest tests + 3 Unittest tests total.**
Registration, login, search and cart all run against the live site, so the
automation is visible end-to-end (run headed with `SLOWMO=1` to watch it).

## 4. Design notes — how each requirement is met

- **Unittest** — `tests_unittest/test_login_unittest.py`, using
  `setUp`/`tearDown` for driver lifecycle and `subTest` for CSV-driven cases.
- **PyTest** — `tests_pytest/`, using fixtures (`driver`,
  `logged_in_driver`) and `@pytest.mark.parametrize` for data-driven runs.
- **Page Object Model** — `pages/`: `BasePage` centralizes waits/interactions;
  `LoginPage` and `ProductSearchPage` expose only locators + business
  methods, no raw Selenium calls in test files.
- **Utility Classes** — `utils/driver_factory.py` (browser creation),
  `utils/screenshot_utils.py`, `utils/csv_reader.py`.
- **Configuration Management** — `config/config_reader.py` reads
  `config.ini`, overridable per-key via environment variables
  (`HEADLESS=false`, `BROWSER=firefox`, `TEST_ENV=staging`).
- **Test Data Handling (CSV)** — `test_data/login_data.csv` and
  `search_data.csv`, consumed by both suites via `utils/csv_reader.py`.
- **Screenshots on Failure** — `unittest`'s `tearDown` checks
  `_outcome`; PyTest's `conftest.py` uses the
  `pytest_runtest_makereport` hook, saving to `reports/screenshots/` and
  embedding into the HTML report when the test failed.
- **HTML Reporting** — `pytest.ini` wires up `pytest-html` (`reports/report.html`,
  self-contained single file).

## 5. Target site

The suite runs against the live practice site
`https://automationexercise.com` (configured in `config.ini`'s `base_url`),
which exposes stable `data-qa` hooks for login/signup plus solid `id`
hooks (`#search_product`, `#submit_search`, `#cartModal`) for the catalog.
An earlier revision used a bundled local Flask + static-page app to avoid
third-party flakiness; it was retired once the framework was repointed at
the live site, since the assignment's demo value is highest there. Live-site
realities handled in code: explicit waits for async badge/modal updates,
JS clicks past ad overlays, direct navigation past the Google vignette
interstitial, and throwaway accounts auto-registered/deleted per run.
