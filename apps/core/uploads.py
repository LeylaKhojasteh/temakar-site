"""ابزارهای مشترک: نام‌گذاری فایل آپلودی، بهینه‌سازی و اعتبارسنجی تصویر.

هر تصویر تازه در سه اندازه ذخیره می‌شود: فایل اصلی (حداکثر ۲۰۰۰ پیکسل)، نسخهٔ
کارت و نسخهٔ بندانگشتی. این کار از دانلود تصویر بزرگ برای یک قاب کوچک جلوگیری می‌کند.
"""

import uuid
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from PIL import Image, ImageOps

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_BYTES = 4 * 1024 * 1024
MAX_IMAGE_DIMENSION = 2000
IMAGE_QUALITY = 82

CARD_SIZE = (800, 500)
THUMB_SIZE = (160, 160)
DERIVATIVE_SIZES = {"card": CARD_SIZE, "thumb": THUMB_SIZE}

_FORMAT_BY_SUFFIX = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
_variant_cache: dict[tuple[str, str], bool] = {}


@dataclass(frozen=True)
class ImageVariant:
    url: str
    width: int
    height: int


@deconstructible
class UploadToFolder:
    """نام فایل را خودمان می‌سازیم؛ نام فایل کاربر هرگز در مسیر نمی‌آید."""

    def __init__(self, folder: str):
        self.folder = folder

    def __call__(self, instance, filename: str) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_IMAGE_EXTENSIONS:
            suffix = ".jpg"
        return f"{self.folder}/{uuid.uuid4().hex}{suffix}"


@deconstructible
class ImageFileSizeValidator:
    """سقف حجم فایل، سمت سرور."""

    def __init__(self, max_bytes: int = MAX_IMAGE_BYTES):
        self.max_bytes = max_bytes

    def __call__(self, value) -> None:
        size = getattr(value, "size", None)
        if size and size > self.max_bytes:
            limit_mb = self.max_bytes // (1024 * 1024)
            raise ValidationError(f"حجم تصویر نباید بیشتر از {limit_mb} مگابایت باشد.")

    def __eq__(self, other) -> bool:
        return isinstance(other, ImageFileSizeValidator) and other.max_bytes == self.max_bytes


def optimize_image(
    uploaded, max_dimension: int = MAX_IMAGE_DIMENSION, quality: int = IMAGE_QUALITY
):
    """تصویر را کوچک و بازکدگذاری می‌کند و دادهٔ EXIF را حذف می‌کند.

    قالب اصلی حفظ می‌شود تا پسوند فایل با محتوای آن یکی بماند.
    """
    uploaded.seek(0)
    with Image.open(uploaded) as image:
        image_format = image.format or "JPEG"
        image = ImageOps.exif_transpose(image)
        if max(image.size) > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

        if image_format == "JPEG":
            image = image.convert("RGB")
            save_kwargs = {"quality": quality, "optimize": True, "progressive": True}
        elif image_format == "PNG":
            save_kwargs = {"optimize": True}
        else:
            save_kwargs = {"quality": quality, "method": 6}

        buffer = BytesIO()
        image.save(buffer, format=image_format, **save_kwargs)
        size = image.size

    buffer.seek(0)
    return buffer, size


def variant_name(original_name: str, kind: str) -> str:
    """نام فایل مشتق‌شده از نام اصلی ساخته می‌شود، نه از نام کاربر."""
    path = Path(original_name)
    return f"{path.parent.as_posix()}/{path.stem}_{kind}{path.suffix.lower()}"


def _save_derivative(field_file, kind: str, size: tuple[int, int]) -> None:
    suffix = Path(field_file.name).suffix.lower()
    image_format = _FORMAT_BY_SUFFIX.get(suffix, "JPEG")
    with field_file.storage.open(field_file.name, "rb") as source:
        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image)
            fitted = ImageOps.fit(image, size, Image.LANCZOS, centering=(0.5, 0.5))
            if image_format == "JPEG":
                fitted = fitted.convert("RGB")
            buffer = BytesIO()
            if image_format == "JPEG":
                fitted.save(buffer, format="JPEG", quality=80, optimize=True, progressive=True)
            elif image_format == "PNG":
                fitted.save(buffer, format="PNG", optimize=True)
            else:
                fitted.save(buffer, format="WEBP", quality=80, method=6)

    target = variant_name(field_file.name, kind)
    if field_file.storage.exists(target):
        field_file.storage.delete(target)
    field_file.storage.save(target, ContentFile(buffer.getvalue()))
    _variant_cache.pop((field_file.name, kind), None)


def store_optimized_image(instance, field_name: str = "image") -> None:
    """تصویر تازه را بهینه می‌کند، ابعاد نهایی را می‌نویسد و مشتق‌ها را می‌سازد."""
    field_file = getattr(instance, field_name)
    optimized, (width, height) = optimize_image(field_file)
    field_file.save(Path(field_file.name).name, ContentFile(optimized.read()), save=False)
    instance.image_width = width
    instance.image_height = height
    for kind, size in DERIVATIVE_SIZES.items():
        _save_derivative(field_file, kind, size)


def image_variant(field_file, kind: str) -> ImageVariant | None:
    """نشانی نسخهٔ مشتق‌شده؛ اگر ساخته نشده باشد، تصویر اصلی برمی‌گردد."""
    if not field_file:
        return None
    size = DERIVATIVE_SIZES.get(kind)
    if size is None:
        return ImageVariant(field_file.url, field_file.width, field_file.height)

    target = variant_name(field_file.name, kind)
    cache_key = (field_file.name, kind)
    if cache_key not in _variant_cache:
        _variant_cache[cache_key] = field_file.storage.exists(target)
    if not _variant_cache[cache_key]:
        return ImageVariant(field_file.url, field_file.width, field_file.height)
    return ImageVariant(field_file.storage.url(target), size[0], size[1])
