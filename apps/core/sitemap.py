"""نقشهٔ سایت دوزبانه با لینک‌های جایگزین (hreflang)."""

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation

from apps.services.models import Service


def _path(name: str, args: tuple, lang: str) -> str:
    with translation.override(lang):
        return reverse(name, args=args)


def _entry(name: str, args: tuple = (), lastmod=None) -> dict:
    return {
        "en": f"{settings.SITE_URL}{_path(name, args, 'en')}",
        "fa": f"{settings.SITE_URL}{_path(name, args, 'fa')}",
        "lastmod": lastmod,
    }


def sitemap_view(request):
    entries = [
        _entry("core:home"),
        _entry("core:who_we_are"),
        _entry("services:index"),
        _entry("contact:page"),
    ]

    services = Service.objects.filter(is_active=True).only("slug", "updated_at")
    for service in services:
        entries.append(_entry("services:detail", (service.slug,), lastmod=service.updated_at))

    return render(
        request,
        "sitemap.xml",
        {"entries": entries},
        content_type="application/xml",
    )
