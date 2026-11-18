"""ذخیره‌سازی رسانه در پایگاه‌داده؛ برای میزبان‌هایی که دیسک پایدار ندارند."""

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".mp4": "video/mp4",
}


def guess_content_type(name: str) -> str:
    for suffix, content_type in CONTENT_TYPES.items():
        if name.lower().endswith(suffix):
            return content_type
    return "application/octet-stream"


@deconstructible
class DatabaseStorage(Storage):
    """فایل‌ها در جدول MediaFile نگهداری می‌شوند و از همان‌جا سرو می‌شوند."""

    def _open(self, name, mode="rb"):
        from apps.core.models import MediaFile

        try:
            stored = MediaFile.objects.get(name=name)
        except MediaFile.DoesNotExist as exc:
            raise FileNotFoundError(name) from exc
        return ContentFile(stored.data, name=name)

    def _save(self, name, content):
        from apps.core.models import MediaFile

        data = content.read()
        if isinstance(data, str):
            data = data.encode()
        content_type = getattr(content, "content_type", "") or guess_content_type(name)
        MediaFile.objects.update_or_create(
            name=name,
            defaults={"data": data, "size": len(data), "content_type": content_type},
        )
        return name

    def exists(self, name):
        from apps.core.models import MediaFile

        return MediaFile.objects.filter(name=name).exists()

    def delete(self, name):
        from apps.core.models import MediaFile

        MediaFile.objects.filter(name=name).delete()

    def size(self, name):
        from apps.core.models import MediaFile

        return MediaFile.objects.values_list("size", flat=True).get(name=name)

    def url(self, name):
        return f"{settings.MEDIA_URL}{name}"

    def path(self, name):
        raise NotImplementedError("فایل‌ها در پایگاه‌داده‌اند و مسیر فیزیکی ندارند.")
