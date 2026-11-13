"""ویوی صفحهٔ تماس و ارسال فرم."""

import logging
import time

from django.core.signing import TimestampSigner
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.core.i18n import language, translate

from .forms import ContactForm
from .notify import notify_new_message
from .throttle import client_ip, hash_ip, is_rate_limited

logger = logging.getLogger(__name__)


def _new_token() -> str:
    return TimestampSigner().sign(str(time.time()))


def _render(request, form=None, *, success: bool = False, status: int = 200):
    """قالب کامل برای مرورگر و قطعهٔ کوچک برای درخواست اچ‌تی‌ام‌ال‌اکس."""
    htmx = request.headers.get("HX-Request") == "true"
    if htmx:
        template = "contact/_success.html" if success else "contact/_form.html"
    else:
        template = "contact/page.html"
    return render(
        request,
        template,
        {
            "form": form,
            "success": success,
            "page_title": translate("meta.contact.title") + translate("meta.suffix"),
            "page_description": translate("meta.contact.desc"),
        },
        status=status,
    )


@require_http_methods(["GET", "POST"])
def page(request):
    lang = language()

    if request.method == "GET":
        if request.GET.get("sent") == "1":
            return _render(request, success=True)
        form = ContactForm(lang=lang, initial={"token": _new_token(), "language": lang})
        return _render(request, form)

    form = ContactForm(request.POST, lang=lang)

    # تلهٔ ربات: پاسخ موفق داده می‌شود ولی چیزی ذخیره نمی‌شود.
    if form.is_honeypot_filled():
        logger.info("فرم تماس: ارسال توسط تلهٔ ربات رد شد.")
        return _render(request, success=True, status=202)

    ip_hash = hash_ip(client_ip(request))

    if is_rate_limited(ip_hash):
        form.add_error(None, translate("form.rate_limited", lang))
        return _render(request, form)

    if not form.is_valid():
        form.mark_error_attributes()
        return _render(request, form)

    try:
        message = form.save(ip_hash=ip_hash)
    except Exception:
        logger.exception("ذخیرهٔ پیام تماس ناموفق بود.")
        form.add_error(None, translate("form.save_failed", lang))
        return _render(request, form)

    notify_new_message(message)

    if request.headers.get("HX-Request") == "true":
        return _render(request, success=True)

    # الگوی «ارسال، سپس تغییر مسیر» تا رفرش صفحه پیام را دوباره ثبت نکند.
    return redirect(f"{reverse('contact:page')}?sent=1")
