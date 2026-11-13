"""مدل‌های عمومی سایت: تنظیمات و شبکه‌های اجتماعی."""

from django.db import models


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
