"""آپلود تصویر داخل متن غنی؛ فقط ستاد مجاز است."""

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.core.uploads import optimize_image

ALLOWED = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def _is_staff(request):
    return request.user.is_authenticated and request.user.is_staff


@require_POST
def upload_inline_image(request):
    if not _is_staff(request):
        return JsonResponse({"error": "forbidden"}, status=403)

    upload = request.FILES.get("image")
    if not upload:
        return JsonResponse({"error": "missing"}, status=400)
    if upload.content_type not in ALLOWED:
        return JsonResponse({"error": "type"}, status=400)
    if upload.size > 4 * 1024 * 1024:
        return JsonResponse({"error": "size"}, status=400)

    optimized, (width, height) = optimize_image(upload)
    suffix = upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else "jpg"
    name = f"inline/{upload.name.rsplit('.', 1)[0]}.{suffix}"
    stored = default_storage.save(name, ContentFile(optimized.read()))
    return JsonResponse({
        "url": default_storage.url(stored),
        "width": width,
        "height": height,
    })
