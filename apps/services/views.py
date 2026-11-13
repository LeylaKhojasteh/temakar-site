"""ویوهای خدمات: فهرست و جزئیات."""

import re

from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags

from apps.core.i18n import localized, translate

from .models import Service

HEADING_RE = re.compile(r"<h3(?P<attrs>[^>]*)>(?P<text>.*?)</h3>", re.S)


def _published_services():
    return Service.objects.filter(is_active=True)


def _with_toc(html: str) -> tuple[str, list[dict]]:
    """به تیترهای h3 شناسه می‌دهد و فهرست درون‌صفحه‌ای می‌سازد."""
    items: list[dict] = []
    if not html:
        return html, items

    def replace(match: re.Match) -> str:
        anchor = f"section-{len(items) + 1}"
        label = strip_tags(match.group("text")).strip()
        items.append({"id": anchor, "label": label})
        return f'<h3 id="{anchor}">{match.group("text")}</h3>'

    return HEADING_RE.sub(replace, html), items


def index(request):
    services = list(_published_services())
    return render(
        request,
        "services/index.html",
        {
            "services": services,
            "page_title": translate("meta.services.title") + translate("meta.suffix"),
            "page_description": translate("meta.services.desc"),
        },
    )


def detail(request, slug: str):
    service = get_object_or_404(_published_services(), slug=slug)
    related = list(_published_services().exclude(pk=service.pk).order_by("order", "id")[:2])
    body = localized(service, "body")
    body_html, toc = _with_toc(body)
    return render(
        request,
        "services/detail.html",
        {
            "service": service,
            "related_services": related,
            "body_html": body_html,
            "toc": toc,
            "page_title": _title(localized(service, "title")),
            "page_description": localized(service, "summary") or translate("meta.services.desc"),
        },
    )


def _title(text: str) -> str:
    return f"{text}{translate('meta.suffix')}"
