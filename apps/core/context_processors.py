"""داده‌های مشترک همهٔ قالب‌ها: تنظیمات سایت، زبان، ناوبری و مسیر معادل زبان دیگر."""

from django.conf import settings
from django.urls import reverse

from apps.core.i18n import language, translate
from apps.core.models import SiteSettings, SocialLink
from apps.services.models import Service


def _strip_language_prefix(path: str) -> str:
    """حذف /fa از ابتدای مسیر تا مسیر لایه‌ای (بدون زبان) به دست آید."""
    if path == "/fa" or path == "/fa/":
        return "/"
    if path.startswith("/fa/"):
        return path[len("/fa") :]
    return path


def _language_paths(path: str) -> dict[str, str]:
    """مسیر همان صفحه در هر دو زبان."""
    neutral = _strip_language_prefix(path)
    return {
        "en": neutral,
        "fa": "/fa/" if neutral == "/" else f"/fa{neutral}",
    }


def _nav_items(path: str) -> list[dict]:
    """آیتم‌های ناوبری با وضعیت فعال؛ آدرس‌ها با پیشوند زبان ساخته می‌شوند."""
    neutral = _strip_language_prefix(path)
    definitions = [
        ("core:home", "nav.home", "/", True),
        ("core:who_we_are", "nav.about", "/who-we-are/", False),
        ("services:index", "nav.services", "/our-services/", False),
        ("contact:page", "nav.contact", "/contact/", False),
    ]
    items = []
    for url_name, label_key, prefix, exact in definitions:
        active = neutral == prefix if exact else neutral.startswith(prefix)
        items.append(
            {
                "url": reverse(url_name),
                "label": translate(label_key),
                "active": active,
            }
        )
    return items


def site_context(request) -> dict:
    lang = language()
    path = request.path
    paths = _language_paths(path)
    site = SiteSettings.load()
    services = (
        []
        if path.startswith("/admin/")
        else list(Service.objects.filter(is_active=True).order_by("order", "id"))
    )

    return {
        "site": site,
        "social_links": SocialLink.objects.filter(is_active=True),
        "service_menu": services,
        "services_url": reverse("services:index"),
        "lang": lang,
        "is_fa": lang == "fa",
        "dir": "rtl" if lang == "fa" else "ltr",
        "nav_items": _nav_items(path),
        "alt_paths": paths,
        "canonical_url": f"{settings.SITE_URL}{path}",
        "site_url": settings.SITE_URL,
        "brand_fa": settings.SITE_NAME,
        "brand_en": settings.SITE_NAME_LATIN,
    }
