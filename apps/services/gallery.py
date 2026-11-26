"""عکسهای اضافی صفحهٔ جزئیات خدمت."""

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.core.uploads import ImageFileSizeValidator, UploadToFolder, store_optimized_image


class ServiceImage(models.Model):
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="gallery",
        verbose_name="خدمت",
    )
    image = models.ImageField(
        "عکس",
        upload_to=UploadToFolder("services/gallery"),
        validators=[ImageFileSizeValidator()],
    )
    image_width = models.PositiveIntegerField(editable=False, default=0)
    image_height = models.PositiveIntegerField(editable=False, default=0)
    caption_fa = models.CharField("عنوان (فارسی)", max_length=160, blank=True)
    caption_en = models.CharField("عنوان (انگلیسی)", max_length=160, blank=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "عکس خدمت"
        verbose_name_plural = "عکسهای خدمت"

    def __str__(self) -> str:
        return f"عکس {self.order} – {self.service}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_image = self.image.name if self.pk and self.image else ""

    def save(self, *args, **kwargs):
        if self.image and self.image.name != self._original_image:
            store_optimized_image(self)
        super().save(*args, **kwargs)
        if self.image:
            self._original_image = self.image.name


@receiver(post_delete, sender=ServiceImage)
def delete_gallery_file(sender, instance, **kwargs):
    """حذف فایل عکس وقتی رکوردش پاک میشود."""
    if instance.image:
        try:
            instance.image.delete(save=False)
        except OSError:
            pass
