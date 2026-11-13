"""مدل خدمت.

هر خدمت یک واحد مستقل است: نامک یکتا، عنوان و متن دوزبانه، تصویر، ترتیب و وضعیت.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.richtext import sanitize_html
from apps.core.uploads import ImageFileSizeValidator, UploadToFolder, store_optimized_image


class Service(models.Model):
    slug = models.SlugField(
        "نامک",
        max_length=90,
        unique=True,
        allow_unicode=False,
        help_text="بخش آدرس صفحه؛ فقط حروف لاتین، رقم و خط تیره.",
    )
    title_en = models.CharField("عنوان (انگلیسی)", max_length=180)
    title_fa = models.CharField("عنوان (فارسی)", max_length=180, blank=True)
    summary_en = models.TextField("خلاصه (انگلیسی)", max_length=400, blank=True)
    summary_fa = models.TextField("خلاصه (فارسی)", max_length=400, blank=True)
    body_en = models.TextField("متن کامل (انگلیسی)", blank=True)
    body_fa = models.TextField("متن کامل (فارسی)", blank=True)
    image = models.ImageField(
        "تصویر",
        upload_to=UploadToFolder("services/items"),
        blank=True,
        validators=[ImageFileSizeValidator()],
    )
    image_width = models.PositiveIntegerField(editable=False, default=0)
    image_height = models.PositiveIntegerField(editable=False, default=0)
    order = models.PositiveSmallIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"
        indexes = [models.Index(fields=["is_active", "order"])]

    def __str__(self) -> str:
        return self.title_fa or self.title_en

    def get_absolute_url(self) -> str:
        return reverse("services:detail", args=[self.slug])

    LOGO_MAP = (
        ("power-transmission", "transmission"),
        ("power-production", "production"),
        ("oil-gas", "oil-gas"),
        ("supply-chain", "consulting"),
    )

    @property
    def logo_template(self) -> str:
        """لوگوی دوبعدی متناسب با موضوع خدمت؛ برای نامک ناشناس، لوگوی ساده."""
        for keyword, name in self.LOGO_MAP:
            if keyword in self.slug:
                return f"partials/logos/{name}.html"
        return "partials/logos/default.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_image = self.image.name if self.pk and self.image else ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)[:90]
        # متن غنی پیش از ذخیره پاک‌سازی می‌شود تا خروجی قالب همیشه امن باشد.
        self.body_en = sanitize_html(self.body_en)
        self.body_fa = sanitize_html(self.body_fa)
        if self.image and self.image.name != self._original_image:
            store_optimized_image(self)
        elif not self.image:
            self.image_width = self.image_height = 0
        super().save(*args, **kwargs)
        if self.image:
            self._original_image = self.image.name
