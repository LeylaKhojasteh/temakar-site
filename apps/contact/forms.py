"""فرم تماس با اعتبارسنجی سمت سرور و محافظت‌های ضد اسپم."""

import time

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, TimestampSigner

from apps.core.i18n import translate

from .models import ContactMessage

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def _lang() -> str:
    from apps.core.i18n import language

    return language()


class ContactForm(forms.Form):
    """فرم عمومی؛ همهٔ برچسب‌ها و پیام‌ها دوزبانه‌اند."""

    name = forms.CharField(
        label="Name",
        max_length=120,
        min_length=2,
        widget=forms.TextInput(attrs={"autocomplete": "name", "class": "field-input"}),
    )
    company = forms.CharField(
        label="Company",
        max_length=160,
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "organization", "class": "field-input"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "dir": "ltr",
                "class": "field-input",
                "inputmode": "email",
            }
        ),
    )
    phone = forms.CharField(
        label="Phone",
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={"autocomplete": "tel", "dir": "ltr", "class": "field-input", "inputmode": "tel"}
        ),
    )
    subject = forms.CharField(
        label="Subject",
        max_length=160,
        min_length=3,
        widget=forms.TextInput(attrs={"class": "field-input"}),
    )
    body = forms.CharField(
        label="Message",
        max_length=5000,
        min_length=10,
        widget=forms.Textarea(attrs={"rows": 6, "class": "field-input field-textarea"}),
    )

    # فیلدهای فنی که کاربر نمی‌بیند.
    language = forms.ChoiceField(
        choices=[("en", "en"), ("fa", "fa")],
        required=False,
        widget=forms.HiddenInput,
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    token = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop("lang", None) or _lang()
        super().__init__(*args, **kwargs)
        self.lang = lang
        self.fields["name"].label = translate("form.name", lang)
        self.fields["company"].label = translate("form.company", lang)
        self.fields["email"].label = translate("form.email", lang)
        self.fields["phone"].label = translate("form.phone", lang)
        self.fields["subject"].label = translate("form.subject", lang)
        self.fields["body"].label = translate("form.body", lang)

        required_message = "این فیلد الزامی است." if lang == "fa" else "This field is required."
        for field in self.fields.values():
            field.error_messages["required"] = required_message

        self.fields["name"].error_messages.update(
            {
                "min_length": "نام باید حداقل ۲ نویسه باشد."
                if lang == "fa"
                else "Name is too short.",
                "max_length": "نام بیش از حد بلند است." if lang == "fa" else "Name is too long.",
            }
        )
        self.fields["email"].error_messages.update(
            {
                "invalid": "نشانی ایمیل معتبر نیست."
                if lang == "fa"
                else "Enter a valid email address.",
            }
        )
        self.fields["subject"].error_messages.update(
            {
                "min_length": "موضوع باید حداقل ۳ نویسه باشد."
                if lang == "fa"
                else "Subject is too short.",
            }
        )
        self.fields["body"].error_messages.update(
            {
                "min_length": "متن پیام باید حداقل ۱۰ نویسه باشد."
                if lang == "fa"
                else "Message is too short.",
                "max_length": "متن پیام بیش از حد بلند است."
                if lang == "fa"
                else "Message is too long.",
            }
        )
        self.fields["language"].initial = lang

    def clean_phone(self) -> str:
        value = (self.cleaned_data.get("phone") or "").translate(PERSIAN_DIGITS).strip()
        if not value:
            return ""
        allowed = set("0123456789+ -()")
        if any(char not in allowed for char in value):
            raise ValidationError(
                "شمارهٔ تلفن فقط می‌تواند شامل رقم، فاصله، خط تیره و + باشد."
                if self.lang == "fa"
                else "Phone can only contain digits, spaces, hyphens, parentheses and +."
            )
        if len(value) < 6:
            raise ValidationError(
                "شمارهٔ تلفن کوتاه است." if self.lang == "fa" else "Phone number is too short."
            )
        return value

    def clean_token(self) -> str:
        """زمان پر کردن فرم بررسی می‌شود: نه خیلی سریع، نه منقضی."""
        value = self.cleaned_data.get("token") or ""
        if not value:
            raise ValidationError(translate("form.expired", self.lang))
        try:
            stamp = TimestampSigner().unsign(value, max_age=60 * 60 * 2)
        except BadSignature as exc:
            raise ValidationError(translate("form.expired", self.lang)) from exc
        try:
            elapsed = time.time() - float(stamp)
        except ValueError as exc:
            raise ValidationError(translate("form.expired", self.lang)) from exc
        if elapsed < settings.CONTACT_MIN_FILL_SECONDS:
            raise ValidationError(translate("form.too_fast", self.lang))
        return value

    def is_honeypot_filled(self) -> bool:
        return bool((self.data.get("website") or "").strip())

    def mark_error_attributes(self) -> None:
        """فیلدهای خطادار برای صفحه‌خوان قابل تشخیص می‌شوند."""
        for name in self.errors:
            if name not in self.fields:
                continue
            widget = self.fields[name].widget
            auto_id = self[name].auto_id
            widget.attrs["aria-invalid"] = "true"
            widget.attrs["aria-describedby"] = f"{auto_id}_error"

    def save(self, ip_hash: str = "") -> ContactMessage:
        data = self.cleaned_data
        return ContactMessage.objects.create(
            name=data["name"].strip(),
            company=(data.get("company") or "").strip(),
            email=data["email"].strip(),
            phone=(data.get("phone") or "").strip(),
            subject=data["subject"].strip(),
            body=data["body"].strip(),
            language=self.lang,
            ip_hash=ip_hash,
        )
