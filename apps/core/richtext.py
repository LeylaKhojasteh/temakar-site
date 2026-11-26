"""پاک‌سازی HTML متن‌های غنی.

ادمین متن را با ویرایشگر HTML می‌نویسد؛ پیش از ذخیره، تگ‌ها به فهرست مجاز
محدود می‌شوند تا خروجی همیشه امن باشد.
"""

import nh3

ALLOWED_TAGS = {
    "p",
    "br",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "ul",
    "ol",
    "li",
    "a",
    "h2",
    "h3",
    "blockquote",
    "img",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title", "target"},
    "img": {"src", "alt", "width", "height"},
}


def sanitize_html(value: str) -> str:
    """حذف تگ‌ها و ویژگی‌های غیرمجاز از HTML."""
    if not value:
        return ""
    return nh3.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes={"http", "https", "mailto", "tel"},
        link_rel="noopener noreferrer",
    ).strip()


def looks_empty(value: str) -> bool:
    """آیا متن بعد از حذف تگ‌ها خالی است؟"""
    stripped = nh3.clean(value or "", tags=set(), attributes={}, strip_comments=True)
    return not stripped.strip()
