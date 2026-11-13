"""تنظیمات مشترک تست‌ها.

Playwright همگام یک حلقهٔ رویداد در همان رشته بالا می‌آورد؛ برای همین جنگو باید
اجازهٔ دسترسی ORM در این حالت را داشته باشد. فقط در تست فعال است.
"""

import os

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
