"""وارد کردن تصویرهای صفحه‌ها از یک پوشه.

نام فایل‌ها با کلید جایگاه‌ها یکی می‌شود: logo، home_about (یا home-about)،
about، services، contact. پسوندهای مجاز: jpg، jpeg، png و webp.
"""

from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from apps.core.models import SiteImage

ALIASES = {
    "logo": SiteImage.Key.LOGO,
    "home_about": SiteImage.Key.HOME_ABOUT,
    "home-about": SiteImage.Key.HOME_ABOUT,
    "about": SiteImage.Key.ABOUT,
    "services": SiteImage.Key.SERVICES,
    "contact": SiteImage.Key.CONTACT,
}
SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


class Command(BaseCommand):
    help = "تصاویر جایگاه‌های صفحه را از یک پوشه در پنل ثبت می‌کند."

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
            key = ALIASES.get(file.stem.lower())
            if not key:
                continue
            found += 1
            if options["dry_run"]:
                self.stdout.write(f"{file.name} -> {key}")
                continue
            image, created = SiteImage.objects.get_or_create(
                key=key,
                defaults={"alt_fa": "", "alt_en": ""},
            )
            with file.open("rb") as handle:
                image.image.save(file.name, ContentFile(handle.read()), save=False)
            image.save()
            state = "ساخته شد" if created else "به‌روز شد"
            self.stdout.write(self.style.SUCCESS(f"{file.name} -> {key}: {state}"))

        if not found:
            self.stdout.write(self.style.WARNING("هیچ فایلی با نام جایگاه‌ها پیدا نشد."))
