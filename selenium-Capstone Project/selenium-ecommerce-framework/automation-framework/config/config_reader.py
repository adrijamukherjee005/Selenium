"""
Centralised configuration management.

Reads config/config.ini and lets any setting be overridden by an
environment variable of the same name (upper-cased), e.g.:

    TEST_ENV=staging BROWSER=firefox HEADLESS=false pytest
"""
import os
import configparser


class ConfigReader:
    _config = None

    @classmethod
    def _load(cls):
        if cls._config is None:
            parser = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(__file__), "config.ini")
            parser.read(config_path)
            env = os.environ.get("TEST_ENV", "DEFAULT")
            cls._config = parser[env] if env in parser else parser["DEFAULT"]
        return cls._config

    @classmethod
    def get(cls, key, fallback=None):
        # Environment variable always wins, e.g. HEADLESS=false
        env_override = os.environ.get(key.upper())
        if env_override is not None:
            return env_override
        return cls._load().get(key, fallback)

    @classmethod
    def get_bool(cls, key, fallback=False):
        value = cls.get(key, str(fallback))
        return str(value).strip().lower() in ("1", "true", "yes", "on")

    @classmethod
    def get_int(cls, key, fallback=0):
        return int(float(cls.get(key, str(fallback))))

    @classmethod
    def get_float(cls, key, fallback=0.0):
        try:
            return float(cls.get(key, str(fallback)))
        except (TypeError, ValueError):
            return float(fallback)

    # Convenience shortcuts used throughout the framework
    @classmethod
    def base_url(cls):
        return cls.get("base_url", "http://localhost:8080")

    @classmethod
    def api_base_url(cls):
        return cls.get("api_base_url", "http://localhost:5001/api")

    @classmethod
    def browser(cls):
        return cls.get("browser", "chrome")

    @classmethod
    def headless(cls):
        return cls.get_bool("headless", True)

    @classmethod
    def implicit_wait(cls):
        return cls.get_int("implicit_wait", 10)

    @classmethod
    def explicit_wait(cls):
        return cls.get_int("explicit_wait", 15)

    @classmethod
    def page_load_timeout(cls):
        return cls.get_int("page_load_timeout", 30)

    @classmethod
    def slowmo(cls):
        """Extra pause (seconds) after each browser action so headed runs
        are watchable. Set via env, e.g. SLOWMO=1. Default 0 (full speed)."""
        return cls.get_float("slowmo", 0.0)

    @classmethod
    def keep_open_seconds(cls):
        """Keep the browser open this many seconds after each test before
        quitting, so you can inspect the final page. Set via env, e.g.
        KEEP_OPEN_SECONDS=10 or KEEP_OPEN=true (defaults to 15s)."""
        explicit = cls.get("keep_open_seconds", None)
        if explicit is not None:
            try:
                return max(0, int(float(explicit)))
            except (TypeError, ValueError):
                return 0
        return 15 if cls.get_bool("keep_open", False) else 0
