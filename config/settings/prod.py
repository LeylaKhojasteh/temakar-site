"""تنظیمات پروداکشن.

در بوت، متغیرهای ضروری بررسی می‌شوند تا سرویس با تنظیم ناقص بالا نیاید.
"""

from .base import *  # noqa: F401,F403

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")  # noqa: F405

if len(SECRET_KEY) < 50 or SECRET_KEY.startswith("dev-"):
    raise RuntimeError("DJANGO_SECRET_KEY پروداکشن باید تصادفی و حداقل ۵۰ کاراکتر باشد.")

if not DATABASES["default"]["PASSWORD"]:  # noqa: F405
    raise RuntimeError("POSTGRES_PASSWORD برای پروداکشن تنظیم نشده است.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")  # noqa: F405

if not ALLOWED_HOSTS:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS برای پروداکشن تنظیم نشده است.")

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", SITE_URL)  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)  # noqa: F405
SECURE_HSTS_SECONDS = int(env("DJANGO_HSTS_SECONDS", "31536000"))  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# هشدار زودهنگام: بدون ایمیل واقعی، پیام‌ها فقط در دیتابیس می‌مانند.
if EMAIL_BACKEND.endswith("console.EmailBackend"):  # noqa: F405
    import warnings

    warnings.warn(
        "EMAIL_BACKEND روی console است؛ در پروداکشن ایمیل واقعی ارسال نمی‌شود.",
        stacklevel=1,
    )
