"""آماده‌سازی لوگوی همکاران: حذف پس‌زمینه و یکسان‌سازی قاب."""

from io import BytesIO

from PIL import Image, ImageDraw

LOGO_CANVAS = (600, 300)
LOGO_TOLERANCE = 34


def _clear_corners(image: Image.Image) -> Image.Image:
    """پس‌زمینهٔ یکدست را از گوشه‌ها شفاف می‌کند، بدون دست‌زدن به داخل لوگو."""
    rgba = image.convert("RGBA")
    width, height = rgba.size
    for corner in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        try:
            ImageDraw.floodfill(rgba, corner, (0, 0, 0, 0), thresh=LOGO_TOLERANCE)
        except (ValueError, IndexError):
            continue
    return rgba


def _fit_on_canvas(image: Image.Image) -> Image.Image:
    alpha = image.split()[-1]
    box = alpha.getbbox()
    if box:
        image = image.crop(box)

    canvas_w, canvas_h = LOGO_CANVAS
    margin = int(canvas_w * 0.04)
    max_w = canvas_w - margin * 2
    max_h = canvas_h - margin * 2

    scale = min(max_w / image.width, max_h / image.height)
    new_size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    image = image.resize(new_size, Image.LANCZOS)

    canvas = Image.new("RGBA", LOGO_CANVAS, (0, 0, 0, 0))
    canvas.paste(image, ((canvas_w - new_size[0]) // 2, (canvas_h - new_size[1]) // 2), image)
    return canvas


def prepare_logo(image: Image.Image) -> tuple[bytes, int, int]:
    """لوگو را با پس‌زمینهٔ شفاف و روی بوم یکسان برمی‌گرداند."""
    cleared = _clear_corners(image)
    fitted = _fit_on_canvas(cleared)

    buffer = BytesIO()
    fitted.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue(), fitted.width, fitted.height
