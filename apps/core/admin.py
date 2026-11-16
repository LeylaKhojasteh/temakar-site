"""پنل ادمین بخش عمومی: تنظیمات سایت و شبکه‌های اجتماعی."""

from django.contrib import admin
from django.utils.html import format_html

from django.contrib.auth.models import Group, User

from .models import Partner, SiteImage, SiteSettings, SocialLink
from .uploads import image_variant

admin.site.site_header = "مدیریت تماکار"
admin.site.site_title = "تماکار"
admin.site.index_title = "پنل مدیریت"

for _model in (Group, User):
    try:
        admin.site.unregister(_model)
    except admin.sites.NotRegistered:
        pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone", "email", "updated_at")
    fieldsets = (
        ("اطلاعات تماس", {"fields": ("phone", "phone_secondary", "email")}),
        ("نشانی", {"fields": ("address_fa", "address_en")}),
        ("نقشه", {"fields": ("map_query", "map_url")}),
    )

    def has_add_permission(self, request) -> bool:
        # همیشه یک رکورد تنظیمات وجود دارد.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label_fa", "label_en", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ("key", "thumb", "updated_at")
    readonly_fields = ("preview", "image_width", "image_height", "updated_at")
    fieldsets = (
        ("جایگاه", {"fields": ("key",)}),
        ("تصویر", {"fields": ("image", "preview", "image_width", "image_height")}),
        ("متن جایگزین", {"fields": ("alt_fa", "alt_en")}),
        ("زمان", {"fields": ("updated_at",)}),
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

    @admin.display(description="پیش‌نمایش")
    def preview(self, obj):
        if not obj.image:
            return "-"
        return format_html(
            '<img src="{}" width="320" alt="" class="admin-preview">',
            obj.image.url,
        )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("thumb", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    fields = ("logo", "order", "is_active")

    @admin.display(description="لوگو")
    def thumb(self, obj):
        if not obj.logo:
            return "-"
        variant = image_variant(obj.logo, "thumb")
        return format_html(
            '<img class="admin-thumb" src="{}" width="64" height="40" alt="" style="object-fit:contain">',
            variant.url,
        )
