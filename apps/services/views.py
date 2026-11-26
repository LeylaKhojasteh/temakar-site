"""ویوهای خدمات: فهرست و جزئیات."""

import re

from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django.utils import translation

from apps.core.i18n import localized, translate

from .models import Service

HEADING_RE = re.compile(r"<h3(?P<attrs>[^>]*)>(?P<text>.*?)</h3>", re.S)
# نشانهٔ عکس در متن: [عکس: 1] / [photo: 1] — شماره، ترتیب عکس است
PHOTO_RE = re.compile(r"\[(?:عکس|photo)\s*:\s*(\d+)\]", re.I)


def _published_services():
    return Service.objects.filter(is_active=True)


def _with_toc(html: str) -> tuple[str, list[dict]]:
    """به تیترهای h3 شناسه میدهد و فهرست درونصفحهای میسازد."""
    items: list[dict] = []
    if not html:
        return html, items

    def replace(match: re.Match) -> str:
        anchor = f"section-{len(items) + 1}"
        label = strip_tags(match.group("text")).strip()
        items.append({"id": anchor, "label": label})
        return f'<h3 id="{anchor}">{match.group("text")}</h3>'

    return HEADING_RE.sub(replace, html), items


def _photo_html(photo, lang: str) -> str:
    caption = photo.caption_fa if lang == "fa" else photo.caption_en
    caption_html = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (
        '<figure class="inline-photo">'
        f'<img src="{photo.image.url}" width="{photo.image_width}" '
        f'height="{photo.image_height}" alt="{caption or ""}" loading="lazy" decoding="async">'
        f"{caption_html}</figure>"
    )


def detail(request, slug: str):
    service = get_object_or_404(_published_services(), slug=slug)
    # زبان را از مسیر میگیریم تا متن درست خوانده شود، فارغ از زبان active
    lang = "fa" if request.path.startswith("/fa") else "en"
    with translation.override(lang):
        body = localized(service, "body")
    body_html, toc = _with_toc(body)
    gallery = list(service.gallery.all())
    by_order = {photo.order: photo for photo in gallery}

    # هر نشانهٔ [عکس: N] دقیقاً با عکس شمارهٔ N جایگزین میشود.
    def inject(match: re.Match) -> str:
        photo = by_order.get(int(match.group(1)))
        return _photo_html(photo, lang) if photo else ""

    body_html = PHOTO_RE.sub(inject, body_html)

    return render(
        request,
        "services/detail.html",
        {
            "service": service,
            "body_html": body_html,
            "gallery": gallery,
            "toc": toc,
            "page_title": _title(localized(service, "title")),
            "page_description": localized(service, "summary") or translate("meta.services.desc"),
        },
    )


def _title(text: str) -> str:
    return f"{text}{translate('meta.suffix')}"
