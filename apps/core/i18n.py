"""
ترجمهٔ رشته‌های ثابت رابط کاربری.

روی ویندوز ابزار gettext (xgettext/msgfmt) نصب نیست، پس به‌جای فایل‌های .po
یک دیکشنری صریح داریم: بدون مرحلهٔ بیلد، قابل جست‌وجو و قابل بررسی در تست.
متن محتوایی (عنوان خدمت، متن بدنه) در مدل‌ها و با فیلدهای en/fa نگه‌داری می‌شود.
"""

from django.utils.translation import get_language

# هر کلید باید هر دو زبان را داشته باشد؛ تست این را بررسی می‌کند.
STRINGS: dict[str, dict[str, str]] = {
    # ناوبری و برند
    "nav.home": {"en": "Home", "fa": "خانه"},
    "nav.about": {"en": "Who we are", "fa": "ما کی هستیم"},
    "nav.services": {"en": "Our services", "fa": "خدمات ما"},
    "nav.contact": {"en": "Contact us", "fa": "تماس با ما"},
    "nav.menu": {"en": "Menu", "fa": "منو"},
    "nav.close": {"en": "Close", "fa": "بستن"},
    "nav.skip": {"en": "Skip to content", "fa": "رفتن به محتوای اصلی"},
    # دکمه‌ها و پیوندهای عمومی
    "cta.contact": {"en": "Contact us", "fa": "تماس با ما"},
    "cta.services": {"en": "See our services", "fa": "دیدن خدمات"},
    "cta.all_services": {"en": "All services", "fa": "همهٔ خدمات"},
    "cta.about": {"en": "More about Temakar", "fa": "بیشتر دربارهٔ تماکار"},
    "cta.back_to_services": {"en": "All services", "fa": "همهٔ خدمات"},
    "cta.send_message": {"en": "Send message", "fa": "ارسال پیام"},
    # صفحهٔ اصلی
    # ما کی هستیم
    # خدمات
    "services.list.title": {"en": "All services", "fa": "فهرست خدمات"},
    "services.empty": {
        "en": "No services are published in this view yet.",
        "fa": "در این نما هنوز خدمتی منتشر نشده است.",
    },
    # تماس
    "contact.info.title": {"en": "Contact details", "fa": "اطلاعات تماس"},
    "contact.form.title": {"en": "Send us a message", "fa": "پیام بفرستید"},
    "contact.phone": {"en": "Phone", "fa": "تلفن"},
    "contact.email": {"en": "Email", "fa": "ایمیل"},
    "contact.address": {"en": "Address", "fa": "نشانی"},
    "contact.social": {"en": "Social", "fa": "شبکه‌های اجتماعی"},
    "contact.map.open": {"en": "Open in Google Maps", "fa": "باز کردن در گوگل‌مپ"},
    # فرم تماس
    "form.name": {"en": "Your name", "fa": "نام"},
    "form.company": {"en": "Company", "fa": "شرکت"},
    "form.email": {"en": "Your e-mail", "fa": "ایمیل"},
    "form.phone": {"en": "Phone", "fa": "تلفن"},
    "form.subject": {"en": "Subject", "fa": "موضوع"},
    "form.body": {"en": "Message", "fa": "متن پیام"},
    "form.optional": {"en": "optional", "fa": "اختیاری"},
    "form.success.title": {"en": "Your message was received", "fa": "پیام شما ثبت شد"},
    "form.success.body": {
        "en": "We have your message. If you left an email address, we will reply to it.",
        "fa": "پیام شما ثبت شد. اگر ایمیل داده باشی، پاسخ را به همان ایمیل می‌فرستیم.",
    },
    "form.success.again": {"en": "Send another message", "fa": "ارسال پیام دیگر"},
    "form.error.summary": {
        "en": "Some fields need attention. Check the marked fields.",
        "fa": "چند مورد نیاز به اصلاح دارد. فیلدهای علامت‌خورده را ببینید.",
    },
    "form.rate_limited": {
        "en": "Too many messages from this connection. Try again later.",
        "fa": "پیام‌های زیادی از این اتصال ثبت شده است. کمی بعد دوباره تلاش کنید.",
    },
    "form.too_fast": {
        "en": "The form was sent too quickly. Please try again.",
        "fa": "فرم خیلی سریع ارسال شد. لطفاً دوباره تلاش کنید.",
    },
    "form.expired": {
        "en": "This form has expired. Reload the page and try again.",
        "fa": "اعتبار این فرم تمام شده است. صفحه را دوباره بارگذاری کنید.",
    },
    "form.save_failed": {
        "en": "We could not save your message. Please try again, or call us.",
        "fa": "پیام شما ذخیره نشد. دوباره تلاش کنید یا تلفنی تماس بگیرید.",
    },
    # خطاها و عمومی
    "error.404.title": {"en": "Page not found", "fa": "صفحه پیدا نشد"},
    "error.404.body": {
        "en": "The address does not exist or the page has moved.",
        "fa": "این نشانی وجود ندارد یا صفحه جابه‌جا شده است.",
    },
    "error.500.title": {"en": "Something went wrong", "fa": "خطایی پیش آمد"},
    "error.500.body": {
        "en": "The page could not be shown. Try again in a moment, or contact us.",
        "fa": "نمایش این صفحه ممکن نشد. کمی بعد دوباره تلاش کنید یا با ما تماس بگیرید.",
    },
    "error.back_home": {"en": "Back to home", "fa": "بازگشت به خانه"},
    "footer.rights": {"en": "All rights reserved.", "fa": "همهٔ حقوق محفوظ است."},
    "footer.nav_title": {"en": "Pages", "fa": "صفحه‌ها"},
    # عنوان و توضیح صفحه‌ها (برای عنوان مرورگر و متا)
    "meta.suffix": {"en": " | Temakar", "fa": " | تماکار"},
    "meta.home.title": {"en": "Temakar | Industrial engineering", "fa": "تماکار | مهندسی صنعتی"},
    "meta.home.desc": {
        "en": "Temakar supplies materials, equipment and parts for the energy industry: power plants, oil, gas and petrochemicals.",
        "fa": "تماکار تأمین‌کنندهٔ مواد، تجهیزات و قطعات صنعت انرژی است: نیروگاه‌ها، نفت، گاز و پتروشیمی.",
    },
    "meta.about.title": {"en": "Who we are", "fa": "ما کی هستیم"},
    "meta.about.desc": {
        "en": "About Temakar: path, mission, vision and how we work.",
        "fa": "معرفی تماکار: مسیر کاری، مأموریت، چشم‌انداز و اصول کار.",
    },
    "meta.services.title": {"en": "Our services", "fa": "خدمات ما"},
    "meta.services.desc": {
        "en": "The services Temakar provides for the energy industry.",
        "fa": "خدماتی که تماکار برای صنعت انرژی ارائه می‌کند.",
    },
    "meta.contact.title": {"en": "Contact", "fa": "تماس با ما"},
    "meta.contact.desc": {
        "en": "Temakar address, phone and contact form.",
        "fa": "نشانی، تلفن و فرم تماس تماکار.",
    },
    "meta.404.title": {"en": "Page not found", "fa": "صفحه پیدا نشد"},
    "meta.404.desc": {
        "en": "The address does not exist or the page has moved.",
        "fa": "این نشانی وجود ندارد یا صفحه جابه‌جا شده است.",
    },
    "meta.500.title": {"en": "Something went wrong", "fa": "خطایی پیش آمد"},
    "meta.500.desc": {
        "en": "The page could not be shown.",
        "fa": "نمایش این صفحه ممکن نشد.",
    },
}


def language() -> str:
    """زبان فعال درخواست؛ اگر تنظیم نشده باشد انگلیسی."""
    lang = get_language() or "en"
    return "fa" if str(lang).startswith("fa") else "en"


def translate(key: str, lang: str | None = None) -> str:
    """رشتهٔ ترجمه‌شده برای کلید داده‌شده."""
    lang = lang or language()
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(lang) or entry.get("en") or key


def localized(obj, field: str) -> str:
    """مقدار فیلد دوزبانهٔ مدل به زبان جاری (با بازگشت به انگلیسی)."""
    lang = language()
    return getattr(obj, f"{field}_{lang}", "") or getattr(obj, f"{field}_en", "")
