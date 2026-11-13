"""پنل ادمین بخش عمومی: تنظیمات سایت و شبکه‌های اجتماعی."""

from django.contrib import admin

from .models import SiteSettings, SocialLink

admin.site.site_header = "مدیریت تماکار"
admin.site.site_title = "تماکار"
admin.site.index_title = "پنل مدیریت"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone", "email", "updated_at")
    fieldsets = (
        ("اطلاعات تماس", {"fields": ("phone", "email")}),
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
