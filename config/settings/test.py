"""تنظیمات تست.

پیش‌فرض SQLite در حافظه است تا تست‌ها بدون سرور دیتابیس هم اجرا شوند.
برای اجرا روی پستگرس (همان موتور پروداکشن) متغیر TEST_DB=postgres را بده؛
در این حالت اتصال از همان متغیرهای محیطی .env خوانده می‌شود.
"""

import os

from .dev import *  # noqa: F401,F403

if os.environ.get("TEST_DB", "").lower() != "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CONTACT_MIN_FILL_SECONDS = 0

# در تست، فایل‌های استاتیک از پوشه‌های پروژه خوانده شوند (بدون collectstatic).
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
