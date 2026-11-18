"""مدل‌های عمومی سایت: تنظیمات و شبکه‌های اجتماعی."""

from pathlib import Path
from django.db import models

from apps.core.logos import prepare_logo
from apps.core.uploads import ImageFileSizeValidator, UploadToFolder, store_optimized_image


class SiteSettings(models.Model):
    """تنظیمات یکتای سایت؛ همیشه یک رکورد با شناسهٔ ۱."""

    phone = models.CharField("تلفن", max_length=40, blank=True)
    phone_secondary = models.CharField("تلفن دوم", max_length=40, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    address_en = models.CharField("نشانی (انگلیسی)", max_length=240, blank=True)
    address_fa = models.CharField("نشانی (فارسی)", max_length=240, blank=True)
    map_query = models.CharField(
        "عبارت جست‌وجوی نقشه",
        max_length=200,
        blank=True,
        help_text="نشانی یا نام مکان برای جاسازی نقشه، مثلاً «Tehran, Iran».",
    )
    map_url = models.URLField(
        "لینک نقشه",
        blank=True,
        help_text="لینک باز کردن مکان در گوگل‌مپ. خالی بماند، از عبارت نقشه ساخته می‌شود.",
    )
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "SiteSettings":
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance

    def __str__(self) -> str:
        return "تنظیمات سایت"


class SocialLink(models.Model):
    """شبکه‌های اجتماعی نمایش‌داده‌شده در فوتر و صفحهٔ تماس."""

    label_en = models.CharField("برچسب (انگلیسی)", max_length=60)
    label_fa = models.CharField("برچسب (فارسی)", max_length=60)
    url = models.URLField("نشانی")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "شبکهٔ اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"

    def __str__(self) -> str:
        return self.label_fa or self.label_en


class SiteImage(models.Model):
    """تصویرهای مدیریت‌شدهٔ صفحه‌ها (سرصفحه‌ها، نوار خانه و لوگو).

    جای هر تصویر با یک کلید ثابت مشخص است؛ مالک از پنل ادمین برای هر جایگاه
    تصویر می‌گذارد و تا وقتی تصویری نگذاشته باشد، قالب به عکس موقت برمی‌گردد.
    """

    class Key(models.TextChoices):
        LOGO = "logo", "لوگو"
        HOME_ABOUT = "home_about", "نوار دربارهٔ ما (صفحهٔ اصلی)"
        ABOUT = "about", "سرصفحهٔ معرفی شرکت"
        SERVICES = "services", "سرصفحهٔ خدمات"
        CONTACT = "contact", "سرصفحهٔ تماس"

    key = models.CharField(
        "جایگاه",
        max_length=40,
        choices=Key.choices,
        unique=True,
        help_text="هر جایگاه یک تصویر دارد.",
    )
    image = models.ImageField(
        "تصویر",
        upload_to=UploadToFolder("site"),
        validators=[ImageFileSizeValidator()],
        help_text="برای لوگو، PNG با پس‌زمینهٔ شفاف بهتر است.",
    )
    image_width = models.PositiveIntegerField(editable=False, default=0)
    image_height = models.PositiveIntegerField(editable=False, default=0)
    alt_fa = models.CharField("متن جایگزین (فارسی)", max_length=200, blank=True)
    alt_en = models.CharField("متن جایگزین (انگلیسی)", max_length=200, blank=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        ordering = ("key",)
        verbose_name = "تصویر صفحه"
        verbose_name_plural = "تصاویر صفحه‌ها"

    def __str__(self) -> str:
        return self.get_key_display()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_image = self.image.name if self.pk and self.image else ""

    def save(self, *args, **kwargs):
        if self.image and self.image.name != self._original_image:
            store_optimized_image(self)
        elif not self.image:
            self.image_width = self.image_height = 0
        super().save(*args, **kwargs)
        if self.image:
            self._original_image = self.image.name


class Partner(models.Model):
    """لوگوی همکار یا تأمین‌کننده؛ فقط تصویر لازم است."""

    logo = models.ImageField(
        "لوگو",
        upload_to=UploadToFolder("partners"),
        validators=[ImageFileSizeValidator()],
        help_text="PNG با پس‌زمینهٔ شفاف؛ ارتفاع نمایش ۴۴ پیکسل است.",
    )
    image_width = models.PositiveIntegerField(editable=False, default=0)
    image_height = models.PositiveIntegerField(editable=False, default=0)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "همکار"
        verbose_name_plural = "همکاران و تأمین‌کنندگان"

    def __str__(self) -> str:
        return f"لوگوی همکار {self.pk or ''}".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_image = self.logo.name if self.pk and self.logo else ""

    def save(self, *args, **kwargs):
        if self.logo and self.logo.name != self._original_image:
            from io import BytesIO

            from django.core.files.base import ContentFile

            from PIL import Image

            old_name = self.logo.name
            self.logo.seek(0)
            with Image.open(self.logo) as image:
                payload, width, height = prepare_logo(image)
            self.logo.save(
                f"{Path(old_name).stem}-logo.webp",
                ContentFile(payload),
                save=False,
            )
            self.image_width = width
            self.image_height = height
            if old_name and old_name != self.logo.name and self.logo.storage.exists(old_name):
                try:
                    self.logo.storage.delete(old_name)
                except OSError:
                    pass
        super().save(*args, **kwargs)
        if self.logo:
            self._original_image = self.logo.name


class MediaFile(models.Model):
    """فایل رسانه ذخیره‌شده در پایگاه‌داده (برای میزبان بدون دیسک پایدار)."""

    name = models.CharField("نام", max_length=255, unique=True)
    data = models.BinaryField("داده")
    size = models.PositiveIntegerField("حجم", default=0)
    content_type = models.CharField("نوع", max_length=100, blank=True)
    created_at = models.DateTimeField("تاریخ", auto_now_add=True)

    class Meta:
        verbose_name = "فایل رسانه"
        verbose_name_plural = "فایل‌های رسانه"

    def __str__(self) -> str:
        return self.name
