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
    "nav.contact": {"en": "Contact", "fa": "تماس"},
    "nav.menu": {"en": "Menu", "fa": "منو"},
    "nav.close": {"en": "Close", "fa": "بستن"},
    "nav.language_en": {"en": "English", "fa": "انگلیسی"},
    "nav.language_fa": {"en": "Persian", "fa": "فارسی"},
    "nav.skip": {"en": "Skip to content", "fa": "رفتن به محتوای اصلی"},
    "brand.tagline": {"en": "Industrial engineering", "fa": "مهندسی صنعتی"},
    # دکمه‌ها و پیوندهای عمومی
    "cta.contact": {"en": "Contact us", "fa": "تماس با ما"},
    "cta.services": {"en": "See our services", "fa": "دیدن خدمات"},
    "cta.all_services": {"en": "All services", "fa": "همهٔ خدمات"},
    "cta.about": {"en": "More about Temakar", "fa": "بیشتر دربارهٔ تماکار"},
    "cta.back_to_services": {"en": "All services", "fa": "همهٔ خدمات"},
    "cta.send_message": {"en": "Send message", "fa": "ارسال پیام"},
    # صفحهٔ اصلی
    "home.hero.support": {
        "en": "Temakar is an industrial engineering company. This site explains what we do, "
        "how we work, and how to reach us.",
        "fa": "تماکار یک شرکت مهندسی صنعتی است. این سایت نشان می‌دهد چه کاری انجام می‌دهیم، "
        "چطور کار می‌کنیم و چطور می‌توانید با ما در تماس باشید.",
    },
    "home.about.title": {"en": "Who we are", "fa": "ما کی هستیم"},
    "home.about.body": {
        "en": "Temakar works in industrial engineering. We help define a technical need, "
        "choose a workable approach, and follow it through with the people who build it.",
        "fa": "تماکار در حوزهٔ مهندسی صنعتی کار می‌کند. کمک می‌کنیم نیاز فنی روشن شود، "
        "راهکار قابل اجرا انتخاب شود و تا مرحلهٔ اجرا با تیم اجرا همراه می‌مانیم.",
    },
    "home.services.title": {"en": "What we do", "fa": "کاری که انجام می‌دهیم"},
    "home.services.lead": {
        "en": "Our work is organised in categories. Each category holds the services we deliver.",
        "fa": "کار ما در چند دسته سازمان یافته است. هر دسته، خدمت‌های زیرمجموعهٔ خودش را دارد.",
    },
    "home.featured.title": {"en": "Selected services", "fa": "خدمات منتخب"},
    "home.contact.line": {
        "en": "A project, a question, or a technical conversation. Write to us.",
        "fa": "پروژه، پرسش یا یک گفت‌وگوی فنی. برای ما بنویسید.",
    },
    # ما کی هستیم
    "about.lead": {
        "en": "We are an engineering team. Our work starts with a technical question and ends "
        "with something that can be built, checked, and used.",
        "fa": "ما یک تیم مهندسی هستیم. کارمان با یک پرسش فنی شروع می‌شود و به چیزی می‌رسد "
        "که قابل ساخت، قابل بررسی و قابل استفاده باشد.",
    },
    "about.path.title": {"en": "Our path", "fa": "مسیر ما"},
    "about.path.body": {
        "en": "Temakar was formed around a simple idea: engineering decisions should be "
        "explainable. Every recommendation we make has a reason, a calculation or a "
        "test behind it, and we write that reason down for the client.",
        "fa": "تماکار حول یک ایدهٔ ساده شکل گرفته است: تصمیم مهندسی باید قابل توضیح باشد. "
        "هر پیشنهادی که می‌دهیم دلیل، محاسبه یا آزمونی پشتش دارد و همان دلیل را "
        "برای کارفرما می‌نویسیم.",
    },
    "about.mission.title": {"en": "Mission", "fa": "مأموریت"},
    "about.mission.body": {
        "en": "Turn an industrial need into a solution that holds up in operation, not only on paper.",
        "fa": "تبدیل یک نیاز صنعتی به راهکاری که در بهره‌برداری دوام بیاورد، نه فقط روی کاغذ.",
    },
    "about.vision.title": {"en": "Vision", "fa": "چشم‌انداز"},
    "about.vision.body": {
        "en": "Be the engineering partner that clients return to for the next phase of the work.",
        "fa": "اینکه شریک مهندسی باشیم که کارفرما برای مرحلهٔ بعد کار هم دوباره سراغش می‌آید.",
    },
    "about.values.title": {"en": "How we work", "fa": "اصول کار ما"},
    "about.values.1": {
        "en": "We state assumptions instead of hiding them.",
        "fa": "فرض‌ها را می‌نویسیم، پنهان نمی‌کنیم.",
    },
    "about.values.2": {
        "en": "We choose the simplest solution that meets the requirement.",
        "fa": "ساده‌ترین راهکاری را انتخاب می‌کنیم که نیاز را برآورده کند.",
    },
    "about.values.3": {
        "en": "We keep one person accountable for each decision.",
        "fa": "برای هر تصمیم، یک نفر پاسخ‌گو است.",
    },
    # خدمات
    "services.title": {"en": "Our services", "fa": "خدمات ما"},
    "services.lead": {
        "en": "Services are grouped in categories. Open a category to see the services inside it.",
        "fa": "خدمات در چند دسته گروه‌بندی شده‌اند. هر دسته را باز کنید تا خدمات زیرمجموعه را ببینید.",
    },
    "services.list.title": {"en": "All services", "fa": "فهرست خدمات"},
    "services.filter_all": {"en": "All", "fa": "همه"},
    "services.filter_label": {"en": "Filter by category", "fa": "فیلتر بر اساس دسته"},
    "services.empty": {
        "en": "No services are published in this view yet.",
        "fa": "در این نما هنوز خدمتی منتشر نشده است.",
    },
    "services.count": {"en": "services", "fa": "خدمت"},
    # تماس
    "contact.title": {"en": "Contact", "fa": "تماس با ما"},
    "contact.lead": {
        "en": "Write to us about a project, a question or a technical conversation. "
        "We read every message.",
        "fa": "دربارهٔ پروژه، پرسش یا گفت‌وگوی فنی برای ما بنویسید. همهٔ پیام‌ها را می‌خوانیم.",
    },
    "contact.info.title": {"en": "Contact details", "fa": "اطلاعات تماس"},
    "contact.form.title": {"en": "Send us a message", "fa": "پیام بفرستید"},
    "contact.phone": {"en": "Phone", "fa": "تلفن"},
    "contact.email": {"en": "Email", "fa": "ایمیل"},
    "contact.address": {"en": "Address", "fa": "نشانی"},
    "contact.hours": {"en": "Working hours", "fa": "ساعات کاری"},
    "contact.social": {"en": "Social", "fa": "شبکه‌های اجتماعی"},
    "contact.map.title": {"en": "Location on the map", "fa": "موقعیت روی نقشه"},
    "contact.map.open": {"en": "Open in Google Maps", "fa": "باز کردن در گوگل‌مپ"},
    # فرم تماس
    "form.name": {"en": "Your name", "fa": "نام"},
    "form.company": {"en": "Company", "fa": "شرکت"},
    "form.email": {"en": "Your e-mail", "fa": "ایمیل"},
    "form.phone": {"en": "Phone", "fa": "تلفن"},
    "form.subject": {"en": "Subject", "fa": "موضوع"},
    "form.body": {"en": "Message", "fa": "متن پیام"},
    "form.optional": {"en": "optional", "fa": "اختیاری"},
    "form.required": {"en": "required", "fa": "الزامی"},
    "form.submitting": {"en": "Sending", "fa": "در حال ارسال"},
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
    "footer.contact_title": {"en": "Contact", "fa": "تماس"},
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
