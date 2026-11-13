"""گزارش وضعیت محتوا برای تحویل به مالک.

نشان می‌دهد چه چیزی هنوز ناقص است: ترجمهٔ فارسی، تصویر، متن، یا تنظیمات تماس.
این فرمان چیزی را تغییر نمی‌دهد.
"""

from django.core.management.base import BaseCommand

from apps.core.models import SiteSettings
from apps.services.models import Service


class Command(BaseCommand):
    help = "فهرست کمبودهای محتوایی را چاپ می‌کند."

    def handle(self, *args, **options):
        settings_obj = SiteSettings.load()
        missing_settings = [
            label
            for label, value in (
                ("تلفن", settings_obj.phone),
                ("ایمیل", settings_obj.email),
                ("نشانی انگلیسی", settings_obj.address_en),
                ("عبارت نقشه", settings_obj.map_query),
            )
            if not value
        ]

        services = Service.objects.filter(is_active=True)

        no_image = [service.slug for service in services if not service.image]
        no_fa = [service.slug for service in services if not service.title_fa]
        no_fa_body = [service.slug for service in services if not service.body_fa]
        no_en_body = [service.slug for service in services if not service.body_en]
        self.stdout.write(f"خدمات فعال: {services.count()}")
        self.stdout.write("")
        self._section("تنظیمات ناقص", missing_settings)
        self._section("خدمات بدون تصویر", no_image)
        self._section("خدمات بدون عنوان فارسی", no_fa)
        self._section("خدمات بدون متن فارسی", no_fa_body)
        self._section("خدمات بدون متن انگلیسی", no_en_body)

    def _section(self, title: str, items: list[str]) -> None:
        if items:
            self.stdout.write(self.style.WARNING(f"{title} ({len(items)}):"))
            for item in items:
                self.stdout.write(f"  - {item}")
        else:
            self.stdout.write(self.style.SUCCESS(f"{title}: ندارد"))
