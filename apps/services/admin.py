from django import forms
from django.contrib import admin
from django.utils.html import format_html

from apps.core.uploads import image_variant
from apps.core.widgets import RichTextWidget

from .models import Service


class AdminSiteMedia:
    """فایل استایل و اسکریپت کوچک برای فهرست ادمین."""

    class Media:
        css = {"all": ("css/admin-site.css",)}
        js = ("js/admin-list.js",)


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {"body_fa": RichTextWidget, "body_en": RichTextWidget}


@admin.register(Service)
class ServiceAdmin(AdminSiteMedia, admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ("title_en", "thumb", "order", "is_active", "updated_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title_fa", "title_en", "slug", "summary_fa", "summary_en")
    prepopulated_fields = {"slug": ("title_en",)}
    fieldsets = (
        ("شناسه", {"fields": ("slug", "order", "is_active")}),
        ("عنوان و خلاصه", {"fields": ("title_fa", "title_en", "summary_fa", "summary_en")}),
        ("متن کامل", {"fields": ("body_fa", "body_en")}),
        ("تصویر", {"fields": ("image",)}),
    )

    @admin.display(description="تصویر")
    def thumb(self, obj):
        if not obj.image:
            return "-"
        variant = image_variant(obj.image, "thumb")
        return format_html(
            '<img class="admin-thumb" src="{}" width="48" height="48" alt="">',
            variant.url,
        )
