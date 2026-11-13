"""درج محتوای واقعی شرکت از فایل apps/services/content.py.

اجرای دوباره بی‌خطر است: رکوردها با نامک به‌روزرسانی می‌شوند و رکوردهای نمایشی
قدیمی (نامک‌های service-*) غیرفعال می‌شوند، نه حذف.
"""

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import SiteSettings
from apps.services.content import SERVICES, SETTINGS
from apps.services.models import Service


class Command(BaseCommand):
    help = "درج محتوای واقعی خدمات و تنظیمات تماس."

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-images",
            action="store_true",
            help="برای رکوردهای بدون تصویر، عکس نمایشی فعلی را بگذار (تا تحویل عکس‌های واقعی).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        settings_obj = SiteSettings.load()
        for field, value in SETTINGS.items():
            if hasattr(settings_obj, field):
                setattr(settings_obj, field, value)
        settings_obj.save()
        self.stdout.write("تنظیمات تماس به‌روز شد.")

        created = 0
        for index, item in enumerate(SERVICES, start=1):
            service, was_created = Service.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title_en": item["title_en"],
                    "title_fa": item["title_fa"],
                    "summary_en": item["summary_en"],
                    "summary_fa": item["summary_fa"],
                    "body_en": item["body_en"],
                    "body_fa": item["body_fa"],
                    "order": index,
                    "is_active": True,
                },
            )
            created += int(was_created)
            if options["with_images"] and not service.image:
                self._attach_image(service, item["image"])

        # رکوردهای نمایشی قبلی فقط غیرفعال می‌شوند.
        Service.objects.filter(slug__startswith="service-").update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(SERVICES)} خدمت درج یا به‌روز شد ({created} تازه)؛ رکوردهای نمایشی غیرفعال شدند."
            )
        )

    def _attach_image(self, instance, filename: str) -> None:
        from django.conf import settings as django_settings

        source = django_settings.BASE_DIR / "static" / "img" / "demo" / filename
        if source.exists():
            with source.open("rb") as handle:
                instance.image.save(filename, ContentFile(handle.read()), save=True)
