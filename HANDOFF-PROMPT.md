# HANDOFF-PROMPT.md — First Message for a New Workspace

Copy the block below into the first message of the new chat/workspace.
It assumes `AGENTS.md`, `STANDARD.md`, `docs/` and `PRODUCT.md` are already in the repository.

---

```text
این یک ورک‌اسپیس تازه است و می‌خواهم پروژهٔ جدید را با استاندارد کاری موجود بسازیم.

قبل از هر تغییری، این فایل‌ها را کامل بخوان:
1. AGENTS.md
2. STANDARD.md
3. docs/FRONTEND.md
4. docs/BACKEND.md
5. docs/QUALITY.md
6. docs/SECURITY.md
7. docs/DESIGN.md
8. docs/REFERENCES.md
9. PRODUCT.md

سپس، بدون نوشتن کد:
- خلاصهٔ درک خودت از محصول و مخاطب را بده.
- فرض‌ها و ابهام‌های واقعی را فهرست کن.
- معماری پیشنهادی، مدل داده و نقشهٔ صفحه‌ها را بده.
- یک نقشهٔ اجرای مرحله‌ای با معیار پذیرش هر مرحله بده.
- بگو از کدام skill/منبع برای طراحی و بازبینی استفاده می‌کنی.
- قبل از طراحی، mode مربوط به `antislop` را مشخص کن (DURING برای پروژهٔ جدید).

قوانین:
- دقیقاً همان متن و محتوایی را استفاده کن که در PRODUCT.md آمده؛ بازنویسی نکن.
- هیچ صفحه، فیچر، بج، تگ یا بخش اضافه نساز.
- هیچ دادهٔ دمو، lorem، آمار ساختگی یا نظر مشتری جعلی نساز.
- موبایل و دسکتاپ هم‌وزن هستند؛ ۳۲۰/۳۹۰/۷۶۸/۱۴۴۰ را تست کن.
- هر تغییر باید build، lint، tsc و تست مربوطه را پاس کند.
- بعد از هر مرحله گزارش بده: چه شد، چرا، چه تست شد، چه باقی مانده.
- اگر چیزی را تست نکردی، صریح بگو.
- ریشهٔ باگ را توضیح بده، نه فقط patch.
- رمز، توکن و دیتابیس را هیچ‌جا افشا نکن.
- تا تأیید من کد ننویس.

اگر بین این استاندارد و درخواست من تضاد بود، درخواست صریح من اولویت دارد؛ ولی تضاد را قبل از اجرا بگو.
```

---

## Fill `PRODUCT.md` before sending

Use `PRODUCT.template.md`. The more concrete the brief, the less the agent has to guess.
Do not ask the agent to invent brand facts, prices, policies or imagery.
