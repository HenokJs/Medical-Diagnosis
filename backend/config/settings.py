import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


BASE_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = BASE_DIR / "backend"
STORAGE_DIR = BACKEND_DIR / "storage"


def _split_env_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _build_cors_origins() -> list[str]:
    env_origins = os.environ.get("CORS_ORIGINS")
    if env_origins:
        return _split_env_list(env_origins)

    frontend_url = os.environ.get(
        "FRONTEND_URL",
        "https://haramaya-medical-diagnosis-system.vercel.app",
    )

    defaults = [
        frontend_url,
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    return _dedupe(defaults)


def _normalize_database_url(value: str | None) -> str | None:
    if not value:
        return None

    normalized = value
    if normalized.startswith("postgres://"):
        normalized = "postgresql://" + normalized[len("postgres://") :]

    if normalized.startswith("sqlite://"):
        return normalized

    parsed = urlparse(normalized)
    if not parsed.scheme.startswith("postgresql"):
        return normalized

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    hostname = parsed.hostname or ""
    if hostname.endswith("neon.tech") and "sslmode" not in query:
        query["sslmode"] = "require"
        parsed = parsed._replace(query=urlencode(query))
        return urlunparse(parsed)

    return normalized


class Config:
    APP_NAME = "Medical Diagnosis AI System"
    VERSION = "1.0.0"

    SECRET_KEY = os.environ.get("SECRET_KEY")
    JSON_SORT_KEYS = False

    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }

    CORS_ORIGINS = _build_cors_origins()

    MODEL_DIR = os.environ.get(
        "MODEL_DIR", str(BASE_DIR / "ml" / "saved_models")
    )
    DATASET_DIR = os.environ.get("DATASET_DIR", str(BASE_DIR / "ml" / "datasets"))

    LOG_DIR = os.environ.get("LOG_DIR", str(STORAGE_DIR / "logs"))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_REQUESTS = os.environ.get("LOG_REQUESTS", "false").lower() == "true"

    REPORT_DIR = os.environ.get("REPORT_DIR", str(STORAGE_DIR / "reports"))
    REPORT_TEMPLATE_DIR = os.environ.get(
        "REPORT_TEMPLATE_DIR", str(STORAGE_DIR / "reports" / "templates")
    )

    API_PREFIX = "/api/v1"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MODEL_CACHE_ENABLED = True
    PREDICTION_TIMEOUT = 30
    SKIP_MODEL_LOAD = os.environ.get("SKIP_MODEL_LOAD", "false").lower() == "true"

    TOP_K_PREDICTIONS = int(os.environ.get("TOP_K_PREDICTIONS", "3"))
    CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.1"))
    SEVERITY_LEVELS = ["minor", "moderate", "urgent", "critical"]

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED", "false").lower() == "true"
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "100 per hour")

    MEDICAL_DISCLAIMER = (
        "This system provides clinical decision support only. "
        "Results are not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always seek the advice of qualified health providers with any questions regarding medical conditions."
    )


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_ECHO = False
    FLASK_ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "WARNING"
    FLASK_ENV = "production"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SEND_FILE_MAX_AGE_DEFAULT = 31536000


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOG_LEVEL = "DEBUG"
    FLASK_ENV = "testing"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SKIP_MODEL_LOAD = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def _require_env(name: str) -> None:
    if not os.environ.get(name):
        raise ValueError(f"Missing required environment variable: {name}")


def get_config(env: str | None = None):
    env = env or os.environ.get("FLASK_ENV", "development")
    config_class = config.get(env, config["default"])

    if env in {"development", "production"}:
        _require_env("DATABASE_URL")

    if env == "production":
        _require_env("SECRET_KEY")
        _require_env("JWT_SECRET_KEY")

    return config_class
