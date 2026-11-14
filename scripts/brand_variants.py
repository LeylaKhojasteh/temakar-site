"""ساخت نسخهٔ فوتر لوگو و آیکون‌های سایت از فایل اصلی.

در فوتر، بخش آبی لوگو کاغذی می‌شود تا روی زمینهٔ تیره دیده شود، ولی بخش قرمز
رنگ خودش را نگه می‌دارد و کمی روشن‌تر می‌شود. آیکون‌ها روی یک پلاک کاغذی
گرد گوشه می‌نشینند تا در تب مرورگر تیره هم خوانا باشند.

فقط به Pillow نیاز دارد. بعد از هر بار عوض‌کردن لوگو:

    python scripts/brand_variants.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "img" / "brand" / "logo.png"
FOOTER = ROOT / "static" / "img" / "brand" / "logo-light.png"
PAPER = (232, 237, 242)
RED_LIFT = 1.45


def is_red(red: int, green: int, blue: int) -> bool:
    return red > green + 40 and red > blue + 40


def make_footer_variant(source: Image.Image) -> None:
    light = source.copy()
    pixels = light.load()
    for y in range(light.height):
        for x in range(light.width):
            red, green, blue, alpha = pixels[x, y]
            if not alpha:
                continue
            if is_red(red, green, blue):
                pixels[x, y] = (
                    min(255, round(red * RED_LIFT)),
                    min(255, round(green * RED_LIFT) + 30),
                    min(255, round(blue * RED_LIFT) + 26),
                    alpha,
                )
            else:
                pixels[x, y] = (*PAPER, alpha)
    light.save(FOOTER, format="PNG", optimize=True)
    print(f"{FOOTER.name}: {FOOTER.stat().st_size // 1024} KB")


def make_icon(source: Image.Image, size: int, name: str, plate: bool = True) -> None:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if plate:
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            (0, 0, size - 1, size - 1),
            radius=max(2, round(size * 0.2)),
            fill=(*PAPER, 255),
        )
    else:
        canvas.paste((*PAPER, 255), (0, 0, size, size))

    logo = source.copy()
    logo.thumbnail((int(size * 0.72), int(size * 0.72)), Image.LANCZOS)
    canvas.alpha_composite(logo, ((size - logo.width) // 2, (size - logo.height) // 2))
    target = ROOT / "static" / "img" / name
    canvas.save(target, format="PNG", optimize=True)
    print(f"{name}: {target.stat().st_size // 1024} KB")


def main() -> None:
    source = Image.open(LOGO).convert("RGBA")
    make_footer_variant(source)
    make_icon(source, 32, "icon-32.png")
    make_icon(source, 64, "icon-64.png")
    make_icon(source, 180, "icon-touch.png", plate=False)


if __name__ == "__main__":
    main()
