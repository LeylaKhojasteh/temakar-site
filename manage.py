#!/usr/bin/env python
"""ابزار خط فرمان جنگو."""

import os
import sys


def main() -> None:
    # کنسول ویندوز با کدپیج فارسی خروجی را قطع می‌کند، پس UTF-8 اجباری است.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover
        raise ImportError("جنگو نصب نیست. محیط مجازی را فعال کن و requirements را نصب کن.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
