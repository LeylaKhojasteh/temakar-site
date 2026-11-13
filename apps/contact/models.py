"""پیام‌های فرم تماس."""

from django.db import models


class ContactMessage(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "جدید"
        READ = "read", "خوانده‌شده"
        REPLIED = "replied", "پاسخ داده‌شده"

    class Language(models.TextChoices):
        EN = "en", "انگلیسی"
        FA = "fa", "فارسی"

    name = models.CharField("نام", max_length=120)
    company = models.CharField("شرکت", max_length=160, blank=True)
    email = models.EmailField("ایمیل")
    phone = models.CharField("تلفن", max_length=40, blank=True)
    subject = models.CharField("موضوع", max_length=160)
    body = models.TextField("متن پیام", max_length=5000)
    language = models.CharField(
        "زبان فرم",
        max_length=2,
        choices=Language.choices,
        default=Language.FA,
    )
    status = models.CharField(
        "وضعیت",
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
    )
    # فقط برای محدود کردن نرخ ارسال؛ نشانی کامل IP ذخیره نمی‌شود.
    ip_hash = models.CharField("هش IP", max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        indexes = [models.Index(fields=["status", "created_at"])]

    def __str__(self) -> str:
        return f"{self.name} · {self.subject}"
