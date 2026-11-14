"""وارد کردن تصویر خدمت‌ها از یک پوشه.

نام هر فایل باید نامک خدمت باشد (مثلاً power-transmission-material-facilities.jpg)
یا یکی از نام‌های کوتاه: transmission، production، oil-gas، consulting.
"""

from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from apps.services.models import Service

ALIASES = {
    "transmission": "power-transmission-material-facilities",
    "production": "power-production-material-facilities",
    "oil-gas": "oil-gas-petrochemical-material-facilities",
    "oil_gas": "oil-gas-petrochemical-material-facilities",
    "consulting": "supply-chain-marketing-consulting-training",
}
SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


class Command(BaseCommand):
    help = "تصویر هر خدمت را از یک پوشه به همان خدمت وصل می‌کند."

    def add_arguments(self, parser):
        parser.add_argument("folder", help="پوشه‌ای که فایل‌های تصویر در آن است.")
        parser.add_argument("--dry-run", action="store_true", help="فقط نشان بده، ذخیره نکن.")

    def handle(self, *args, **options):
        folder = Path(options["folder"]).expanduser()
        if not folder.is_dir():
            raise CommandError(f"پوشه پیدا نشد: {folder}")

        found = 0
        for file in sorted(folder.iterdir()):
            if not file.is_file() or file.suffix.lower() not in SUFFIXES:
                continue
            stem = ALIASES.get(file.stem.lower(), file.stem.lower())
            service = Service.objects.filter(slug=stem).first()
            if not service:
                continue
            found += 1
            if options["dry_run"]:
                self.stdout.write(f"{file.name} -> {service.slug}")
                continue
            with file.open("rb") as handle:
                service.image.save(file.name, ContentFile(handle.read()), save=False)
            service.save()
            self.stdout.write(self.style.SUCCESS(f"{file.name} -> {service.slug}"))

        if not found:
            self.stdout.write(self.style.WARNING("هیچ فایلی با نامک خدمات پیدا نشد."))
