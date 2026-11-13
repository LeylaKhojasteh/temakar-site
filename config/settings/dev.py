"""تنظیمات توسعهٔ محلی."""

from .base import *  # noqa: F401,F403

DEBUG = env_bool("DJANGO_DEBUG", True)  # noqa: F405

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0", "[::1]", "testserver"]

STORAGES = {
    **STORAGES,  # noqa: F405
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# فقط برای آزمون سریع قالب‌ها، بدون سرور پستگرس؛ پیش‌فرض پروژه پستگرس است.
if env_bool("USE_SQLITE", False):  # noqa: F405
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }
