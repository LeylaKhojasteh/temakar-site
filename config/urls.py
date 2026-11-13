"""مسیرهای اصلی سایت.

زبان پیش‌فرض انگلیسی در ریشه است و فارسی زیر /fa قرار می‌گیرد. بخش‌های مسیر در
هر دو زبان یکسان‌اند تا لینک‌ها قابل حدس و ثابت بمانند؛ فقط پیشوند زبان تغییر می‌کند.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static as static_files
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core import views as core_views
from apps.core.sitemap import sitemap_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", core_views.favicon, name="favicon"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("sitemap.xml", sitemap_view, name="sitemap"),
]

urlpatterns += i18n_patterns(
    path("", include("apps.core.urls")),
    path("our-services/", include("apps.services.urls")),
    path("contact/", include("apps.contact.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static_files(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"
