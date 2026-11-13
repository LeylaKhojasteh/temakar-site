"""پنل پیام‌های تماس: فقط خواندن و تغییر وضعیت."""

from django.contrib import admin
from django.utils.html import format_html

from .models import ContactMessage


@admin.action(description="علامت‌گذاری به‌عنوان خوانده‌شده")
def mark_read(modeladmin, request, queryset):
    queryset.update(status=ContactMessage.Status.READ)


@admin.action(description="علامت‌گذاری به‌عنوان پاسخ داده‌شده")
def mark_replied(modeladmin, request, queryset):
    queryset.update(status=ContactMessage.Status.REPLIED)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "language", "status_badge", "created_at")
    list_filter = ("status", "language", "created_at")
    search_fields = ("name", "email", "company", "subject", "body")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    actions = [mark_read, mark_replied]
    list_per_page = 30

    readonly_fields = (
        "name",
        "company",
        "email",
        "phone",
        "subject",
        "body",
        "language",
        "created_at",
        "updated_at",
    )
    fields = (
        "status",
        "name",
        "company",
        "email",
        "phone",
        "subject",
        "language",
        "body",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request) -> bool:
        # پیام فقط از فرم سایت ساخته می‌شود.
        return False

    @admin.display(description="وضعیت")
    def status_badge(self, obj):
        return format_html(
            '<span class="badge badge--{}">{}</span>', obj.status, obj.get_status_display()
        )
