"""ویوهای صفحهٔ اصلی، ما کی هستیم، فاویکون و صفحه‌های خطا."""

from django.shortcuts import redirect, render
from django.templatetags.static import static

from apps.core.i18n import translate
from apps.services.models import Service


def home(request):
    services = list(Service.objects.filter(is_active=True).order_by("order", "id"))
    return render(
        request,
        "pages/home.html",
        {
            "services": services,
            "page_title": translate("meta.home.title"),
            "page_description": translate("meta.home.desc"),
        },
    )


def who_we_are(request):
    return render(
        request,
        "pages/who_we_are.html",
        {
            "page_title": translate("meta.about.title") + translate("meta.suffix"),
            "page_description": translate("meta.about.desc"),
        },
    )


def favicon(request):
    """مرورگرها همیشه /favicon.ico را می‌خواهند؛ به فایل SVG هدایت می‌شود."""
    return redirect(static("img/icon-32.png") + "?v=2", permanent=True)


def page_not_found(request, exception=None):
    return render(
        request,
        "errors/404.html",
        {
            "page_title": translate("meta.404.title") + translate("meta.suffix"),
            "page_description": translate("meta.404.desc"),
        },
        status=404,
    )


def server_error(request):
    return render(
        request,
        "errors/500.html",
        {
            "page_title": translate("meta.500.title") + translate("meta.suffix"),
            "page_description": translate("meta.500.desc"),
        },
        status=500,
    )
