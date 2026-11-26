"""فرم‌های پنل مدیریت تماکار."""

from django import forms

from apps.core.widgets import RichTextWidget
from apps.core.models import Partner, SiteImage, SiteSettings, SocialLink
from apps.services.models import Service


class SettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "phone",
            "phone_secondary",
            "email",
            "address_fa",
            "address_en",
            "map_query",
            "map_url",
        )
        widgets = {
            "address_fa": forms.TextInput(attrs={"dir": "rtl"}),
            "address_en": forms.TextInput(attrs={"dir": "ltr"}),
        }


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ("label_fa", "label_en", "url", "order", "is_active")


class ImageForm(forms.ModelForm):
    class Meta:
        model = SiteImage
        fields = ("image", "alt_fa", "alt_en")


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ("logo", "order", "is_active")


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            "title_fa",
            "title_en",
            "slug",
            "summary_fa",
            "summary_en",
            "body_fa",
            "body_en",
            "image",
            "order",
            "is_active",
        )
        widgets = {
            "summary_fa": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "summary_en": forms.Textarea(attrs={"rows": 3, "dir": "ltr"}),
            "body_fa": RichTextWidget(attrs={"dir": "rtl"}),
            "body_en": RichTextWidget(attrs={"dir": "ltr"}),
        }
