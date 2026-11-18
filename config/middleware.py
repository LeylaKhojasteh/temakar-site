"""هدرهای امنیتی و سیاست امنیت محتوا.

صفحه‌های عمومی CSP سخت‌گیرانه دارند (بدون inline). پنل ادمین جنگو برای اجرا به
اسکریپت و استایل درون‌خطی نیاز دارد، پس فقط برای مسیر /admin/ شل می‌شود.
"""

from django.conf import settings
from django.utils import translation


class AdminLanguageMiddleware:
    """پنل ادمین همیشه فارسی است؛ سایت عمومی زبان خودش را از مسیر می‌گیرد."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            translation.activate("fa")
        return self.get_response(request)


PUBLIC_CSP = " ".join(
    [
        "default-src 'self';",
        "base-uri 'self';",
        "object-src 'none';",
        "frame-ancestors 'none';",
        "form-action 'self';",
        "img-src 'self' data:;",
        "font-src 'self';",
        "style-src 'self';",
        "script-src 'self';",
        "connect-src 'self';",
        "frame-src https://www.google.com https://maps.google.com;",
        "upgrade-insecure-requests;",
    ]
)

ADMIN_CSP = " ".join(
    [
        "default-src 'self';",
        "base-uri 'self';",
        "object-src 'none';",
        "frame-ancestors 'none';",
        "form-action 'self';",
        "img-src 'self' data: blob:;",
        "font-src 'self' data:;",
        "style-src 'self' 'unsafe-inline';",
        "script-src 'self' 'unsafe-inline';",
        "connect-src 'self';",
    ]
)


class SecurityHeadersMiddleware:
    """تنظیم هدرهای امنیتی که جنگو به‌تنهایی مدیریت نمی‌کند."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        is_admin = request.path.startswith(("/admin/", "/django-admin/"))

        response.setdefault("Content-Security-Policy", ADMIN_CSP if is_admin else PUBLIC_CSP)
        response.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.setdefault("Cross-Origin-Resource-Policy", "same-origin")

        # در توسعه، HTTPS وجود ندارد؛ تنها در پروداکشن اعمال می‌شوند.
        if not settings.DEBUG:
            response.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains; preload",
            )
        return response


class DefaultLanguageMiddleware:
    """برای نشانی‌های بدون پیشوند زبان، همیشه انگلیسی فعال می‌شود."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        from django.utils import translation

        codes = {code for code, _ in settings.LANGUAGES if code != settings.LANGUAGE_CODE}
        first = request.path_info.strip("/").split("/")[0]
        if first not in codes:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        return self.get_response(request)
