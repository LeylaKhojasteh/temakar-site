"""ابزار ویرایش متن غنی برای ادمین (Quill، فایل محلی)."""

from django import forms


class RichTextWidget(forms.Textarea):
    """متن HTML در یک textarea نگه‌داری می‌شود و ویرایشگر روی آن سوار می‌شود."""

    def __init__(self, attrs=None):
        base = {"class": "richtext-source", "data-richtext": "1", "rows": 12}
        if attrs:
            base.update(attrs)
        super().__init__(base)

    class Media:
        css = {"all": ("vendor/quill/quill.snow.css", "css/admin-richtext.css")}
        js = ("vendor/quill/quill.js", "js/admin-richtext.js")
