"""تگ‌های قالبی مشترک: ترجمه، انتخاب فیلد دوزبانه و آدرس نقشه."""

from urllib.parse import quote

from django import template

from apps.core.i18n import language, translate
from apps.core.uploads import image_variant

register = template.Library()


@register.simple_tag
def tr(key: str) -> str:
    """رشتهٔ رابط کاربری به زبان جاری."""
    return translate(key)


@register.simple_tag
def pick(obj, field: str) -> str:
    """مقدار فیلد دوزبانهٔ مدل، مثل title_en یا title_fa."""
    lang = language()
    value = getattr(obj, f"{field}_{lang}", "")
    if not value and lang != "en":
        value = getattr(obj, f"{field}_en", "")
    return value


@register.simple_tag
def map_embed_url(site) -> str:
    """نشانی جاسازی نقشه؛ بدون کلید API و با زبان جاری."""
    query = (site.map_query or "").strip()
    if not query:
        return ""
    return f"https://www.google.com/maps?q={quote(query)}&output=embed&hl={language()}&z=16"


@register.simple_tag
def map_link_url(site) -> str:
    """لینک باز کردن مکان در گوگل‌مپ."""
    if site.map_url:
        return site.map_url
    query = (site.map_query or "").strip()
    if not query:
        return ""
    return f"https://www.google.com/maps/search/?api=1&query={quote(query)}"


@register.filter
def variant(field_file, kind: str):
    """نسخهٔ کوچک تصویر (card یا thumb) با ابعاد درست."""
    return image_variant(field_file, kind)
