"""ارسال ایمیل اطلاع‌رسانی پیام جدید.

ایمیل یک عارضهٔ جانبی است، نه بخشی از تراکنش: اگر ارسال نشد، پیام در دیتابیس
می‌ماند و مدیر آن را در پنل می‌بیند.
"""

import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import ContactMessage

logger = logging.getLogger(__name__)


def notify_new_message(message: ContactMessage) -> None:
    recipient = settings.CONTACT_NOTIFY_EMAIL
    if not recipient:
        return
    subject = f"پیام جدید: {message.subject}"
    body = (
        f"نام: {message.name}\n"
        f"شرکت: {message.company or '-'}\n"
        f"ایمیل: {message.email}\n"
        f"تلفن: {message.phone or '-'}\n"
        f"زبان: {message.language}\n\n"
        f"{message.body}\n"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
    except Exception:
        # پیام ذخیره شده است؛ خطای ایمیل نباید به کاربر نمایش داده شود.
        logger.exception("ارسال ایمیل اطلاع‌رسانی پیام تماس ناموفق بود (id=%s)", message.pk)
