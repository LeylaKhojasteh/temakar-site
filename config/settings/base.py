"""تنظیمات مشترک هر سه محیط.

مقادیر حساس فقط از متغیر محیطی خوانده می‌شوند؛ فایل .env در ریشهٔ پروژه است و
در مخزن ذخیره نمی‌شود.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str | None = None) -> str:
    """خواندن متغیر محیطی با پیام خطای روشن."""
    value = os.environ.get(name, "").strip()
    if value:
        return value
    if default is not None:
        return default
    raise RuntimeError(f"متغیر محیطی «{name}» تنظیم نشده است. فایل .env را کامل کن.")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None or not value.strip():
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- پایه ---------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = False
ALLOWED_HOSTS: list[str] = []

SITE_NAME = "تماکار"
SITE_NAME_LATIN = "Temakar"
SITE_URL = env("SITE_URL", "http://127.0.0.1:8000").rstrip("/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.services",
    "apps.contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.AdminLanguageMiddleware",
    "config.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_context",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "temakar"),
        "USER": env("POSTGRES_USER", "temakar"),
        "PASSWORD": env("POSTGRES_PASSWORD", ""),
        "HOST": env("POSTGRES_HOST", "127.0.0.1"),
        "PORT": env("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# اگر DATABASE_URL تنظیم شده باشد (مثل Neon یا Supabase) از همان استفاده می‌شود.
_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    from urllib.parse import unquote, urlparse

    _parsed = urlparse(_database_url)
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _parsed.path.lstrip("/"),
        "USER": unquote(_parsed.username or ""),
        "PASSWORD": unquote(_parsed.password or ""),
        "HOST": _parsed.hostname or "",
        "PORT": str(_parsed.port or 5432),
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"sslmode": "require"},
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- زبان ---------------------------------------------------------------

LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("fa", "فارسی")]
USE_I18N = True
USE_TZ = True
TIME_ZONE = "Asia/Tehran"

# --- فایل‌ها -------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", str(BASE_DIR / "media")))


STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

MEDIA_STORAGE = os.environ.get("MEDIA_STORAGE", "")
if MEDIA_STORAGE == "db":
    STORAGES["default"] = {"BACKEND": "apps.core.storage.DatabaseStorage"}

# --- امنیت ---------------------------------------------------------------

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 8
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# --- ایمیل ---------------------------------------------------------------

EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "Temakar <no-reply@temakar.local>")
CONTACT_NOTIFY_EMAIL = env("CONTACT_NOTIFY_EMAIL", "")

# --- فرم تماس ------------------------------------------------------------

CONTACT_RATE_LIMIT_MAX = int(env("CONTACT_RATE_LIMIT_MAX", "3"))
CONTACT_RATE_LIMIT_WINDOW = int(env("CONTACT_RATE_LIMIT_WINDOW", "3600"))
CONTACT_MIN_FILL_SECONDS = int(env("CONTACT_MIN_FILL_SECONDS", "3"))

# فقط برای seed دمو در محیط توسعه.
SEED_ADMIN_USERNAME = env("SEED_ADMIN_USERNAME", "admin")
SEED_ADMIN_PASSWORD = env("SEED_ADMIN_PASSWORD", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {asctime} {name} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
