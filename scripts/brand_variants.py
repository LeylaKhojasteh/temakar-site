"""ساخت نسخهٔ روشن لوگو برای فوتر و آیکون‌های سایت از فایل اصلی.

فقط به Pillow نیاز دارد. بعد از هر بار عوض‌کردن Logo، این را اجرا کن:

    python scripts/brand_variants.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "img" / "brand" / "logo.png"
LIGHT = ROOT / "static" / "img" / "brand" / "logo-light.png"
PAPER = (232, 237, 242)


def make_light(source: Image.Image) -> None:
    """همان شکل لوگو، با رنگ کاغذی، برای زمینه‌های تیره."""
    light = source.copy()
    pixels = light.load()
    for y in range(light.height):
        for x in range(light.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha:
                pixels[x, y] = (*PAPER, alpha)
    light.save(LIGHT, format="PNG", optimize=True)
    print(f"{LIGHT.name}: {LIGHT.stat().st_size // 1024} KB")


def make_icon(source: Image.Image, size: int, name: str, background=None) -> None:
    canvas = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
    logo = source.copy()
    logo.thumbnail((int(size * 0.9), int(size * 0.9)), Image.LANCZOS)
    canvas.alpha_composite(logo, ((size - logo.width) // 2, (size - logo.height) // 2))
    target = ROOT / "static" / "img" / name
    canvas.save(target, format="PNG", optimize=True)
    print(f"{name}: {target.stat().st_size // 1024} KB")


def main() -> None:
    source = Image.open(LOGO).convert("RGBA")
    make_light(source)
    make_icon(source, 32, "icon-32.png")
    make_icon(source, 64, "icon-64.png")
    make_icon(source, 180, "icon-touch.png", background=(*PAPER, 255))


if __name__ == "__main__":
    main()
