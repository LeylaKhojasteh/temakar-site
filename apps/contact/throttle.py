"""محدود کردن نرخ ارسال فرم تماس.

محدودیت در دیتابیس شمرده می‌شود تا با چند پروسه یا ری‌استارت از دست نرود.
نشانی IP به‌صورت هش ذخیره می‌شود، نه خام.
"""

import hashlib
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import ContactMessage


def client_ip(request) -> str:
    """IP واقعی کاربر.

    X-Forwarded-For فقط وقتی معتبر است که بدانیم چند پروکسی قابل‌اعتماد جلوی
    برنامه است؛ آن عدد از تنظیمات TRUSTED_PROXY_COUNT خوانده می‌شود. با مقدار
    پیش‌فرض صفر، هدر نادیده گرفته می‌شود تا با جعل هدر، محدودیت دور زده نشود.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    trusted = int(getattr(settings, "TRUSTED_PROXY_COUNT", 0) or 0)
    if forwarded and trusted > 0:
        hops = [part.strip() for part in forwarded.split(",") if part.strip()]
        if len(hops) >= trusted:
            return hops[-trusted]
    return request.META.get("REMOTE_ADDR", "")


def hash_ip(ip: str) -> str:
    """هش یک‌طرفه با کلید سرور؛ برای شمارش کافی است و IP را افشا نمی‌کند."""
    if not ip:
        return ""
    payload = f"{ip}:{settings.SECRET_KEY}".encode()
    return hashlib.sha256(payload).hexdigest()[:40]


def recent_message_count(ip_hash: str) -> int:
    if not ip_hash:
        return 0
    since = timezone.now() - timedelta(seconds=settings.CONTACT_RATE_LIMIT_WINDOW)
    return ContactMessage.objects.filter(ip_hash=ip_hash, created_at__gte=since).count()


def is_rate_limited(ip_hash: str) -> bool:
    return recent_message_count(ip_hash) >= settings.CONTACT_RATE_LIMIT_MAX
