import time

import pytest
from django.core.signing import TimestampSigner
from django.db import IntegrityError
from django.urls import reverse
from django.utils import translation

from apps.core.i18n import STRINGS, translate
from apps.core.richtext import looks_empty, sanitize_html
from apps.services.models import Service


def make_service(**kwargs):
    defaults = {
        "slug": "service-x",
        "title_en": "Service X",
        "title_fa": "خدمت ایکس",
        "summary_en": "Summary",
        "summary_fa": "خلاصه",
        "body_en": "<p>Body</p>",
        "body_fa": "<p>متن</p>",
        "is_active": True,
    }
    defaults.update(kwargs)
    return Service.objects.create(**defaults)


# --- ترجمه و متن غنی ------------------------------------------------------


def test_every_translation_key_has_both_languages():
    missing = [key for key, value in STRINGS.items() if not value.get("en") or not value.get("fa")]
    assert missing == []


def test_translate_falls_back_to_key_for_unknown_key():
    assert translate("no.such.key") == "no.such.key"


def test_sanitize_html_drops_scripts_and_event_handlers():
    dirty = '<p onclick="steal()">سلام<script>alert(1)</script></p>'
    clean = sanitize_html(dirty)
    assert "<script" not in clean
    assert "onclick" not in clean
    assert "سلام" in clean


def test_sanitize_html_keeps_allowed_link_and_adds_rel():
    clean = sanitize_html('<p><a href="https://example.com" target="_blank">لینک</a></p>')
    assert 'href="https://example.com"' in clean
    assert "noopener" in clean


def test_looks_empty_ignores_markup():
    assert looks_empty("<p> </p>") is True
    assert looks_empty("<p>متن</p>") is False


# --- مدل خدمات -------------------------------------------------------------


@pytest.mark.django_db
def test_service_slug_is_unique():
    make_service(slug="dup")
    with pytest.raises(IntegrityError):
        make_service(slug="dup", title_en="Other")


@pytest.mark.django_db
def test_inactive_service_is_hidden(client):
    service = make_service(is_active=False)

    listing = client.get(reverse("services:index"))
    assert service.slug not in listing.content.decode()

    detail = client.get(reverse("services:detail", args=[service.slug]))
    assert detail.status_code == 404


@pytest.mark.django_db
def test_home_lists_the_published_services(client):
    make_service(slug="s-1", title_fa="خدمت یک")
    make_service(slug="s-2", title_fa="خدمت دو")
    archived = make_service(slug="s-3", title_fa="خدمت سه")
    archived.is_active = False
    archived.save()

    response = client.get(reverse("core:home"))

    assert [service.slug for service in response.context["services"]] == ["s-1", "s-2"]


@pytest.mark.django_db
def test_service_logo_matches_its_slug():
    assert (
        "transmission" in make_service(slug="power-transmission-material-facilities").logo_template
    )
    assert "production" in make_service(slug="power-production-material-facilities").logo_template
    assert "oil-gas" in make_service(slug="oil-gas-petrochemical-material-facilities").logo_template
    assert (
        "consulting"
        in make_service(slug="supply-chain-marketing-consulting-training").logo_template
    )
    assert make_service(slug="something-else").logo_template.endswith("default.html")


# --- تنظیمات و مسیرها -----------------------------------------------------


@pytest.mark.django_db
def test_site_settings_always_single_row():
    from apps.core.models import SiteSettings

    first = SiteSettings.load()
    first.phone = "1"
    first.save()
    second = SiteSettings.load()
    second.phone = "2"
    second.save()

    assert SiteSettings.objects.count() == 1
    assert SiteSettings.objects.get().phone == "2"


@pytest.mark.django_db
def test_persian_pages_live_under_fa_prefix(client):
    with translation.override("fa"):
        persian = reverse("core:who_we_are")
    with translation.override("en"):
        english = reverse("core:who_we_are")

    assert persian == "/fa/who-we-are/"
    assert english == "/who-we-are/"

    response = client.get(persian)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'lang="fa"' in html
    assert 'dir="rtl"' in html
    assert 'hreflang="en"' in html


@pytest.mark.django_db
def test_unknown_page_uses_designed_404(client):
    response = client.get("/this-does-not-exist/")
    assert response.status_code == 404
    assert "404" in response.content.decode()


@pytest.mark.django_db
def test_sitemap_lists_both_languages_and_services(client):
    service = make_service(slug="listed-service")

    response = client.get("/sitemap.xml")
    body = response.content.decode()

    assert response.status_code == 200
    assert body.count("<url>") == body.count("</url>")
    assert "/fa/" in body
    assert "xhtml:link" in body
    assert service.slug in body
    assert "<lastmod>" in body


@pytest.mark.django_db
def test_canonical_and_hreflang_are_absolute(client, settings):
    settings.SITE_URL = "https://example.com"
    response = client.get("/fa/contact/")
    html = response.content.decode()
    assert '<link rel="canonical" href="https://example.com/fa/contact/">' in html
    assert 'hreflang="en" href="https://example.com/contact/"' in html


# --- فرم تماس -------------------------------------------------------------


def valid_form_data(**overrides):
    data = {
        "name": "مریم",
        "company": "شرکت نمونه",
        "email": "maryam@example.com",
        "phone": "0912 000 0000",
        "subject": "پرسش فنی",
        "body": "سلام، دربارهٔ این خدمت یک پرسش فنی دارم.",
        "language": "fa",
        "website": "",
        "token": TimestampSigner().sign(str(time.time() - 30)),
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_contact_form_saves_message(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    response = client.post("/fa/contact/", data=valid_form_data())

    assert response.status_code == 302
    from apps.contact.models import ContactMessage

    message = ContactMessage.objects.get()
    assert message.language == "fa"
    assert message.status == ContactMessage.Status.NEW
    assert message.ip_hash
    assert len(message.ip_hash) < 64


@pytest.mark.django_db
def test_contact_form_preserves_values_on_error(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    data = valid_form_data(email="not-an-email")
    response = client.post("/fa/contact/", data=data)

    assert response.status_code == 200
    html = response.content.decode()
    assert "مریم" in html
    assert "شرکت نمونه" in html
    assert "نشانی ایمیل معتبر نیست" in html


@pytest.mark.django_db
def test_contact_form_rejects_too_fast_submission(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 5
    data = valid_form_data(token=TimestampSigner().sign(str(time.time())))
    response = client.post("/fa/contact/", data=data)

    assert response.status_code == 200
    from apps.contact.models import ContactMessage

    assert ContactMessage.objects.count() == 0


@pytest.mark.django_db
def test_contact_honeypot_silently_discards(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    response = client.post("/fa/contact/", data=valid_form_data(website="http://spam.example"))

    assert response.status_code == 202
    from apps.contact.models import ContactMessage

    assert ContactMessage.objects.count() == 0


@pytest.mark.django_db
def test_contact_rate_limit_blocks_fourth_message(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    settings.CONTACT_RATE_LIMIT_MAX = 3

    for _ in range(3):
        assert client.post("/fa/contact/", data=valid_form_data()).status_code == 302

    response = client.post("/fa/contact/", data=valid_form_data())
    assert response.status_code == 200
    assert "پیام‌های زیادی" in response.content.decode()


@pytest.mark.django_db
def test_contact_htmx_post_returns_partial(client, settings):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    response = client.post(
        "/fa/contact/",
        data=valid_form_data(),
        headers={"HX-Request": "true"},
    )
    assert response.status_code == 200
    body = response.content.decode()
    assert "<html" not in body
    assert "پیام شما ثبت شد" in body


@pytest.mark.django_db
def test_contact_success_page_via_redirect(client):
    response = client.get("/fa/contact/?sent=1")
    assert response.status_code == 200
    assert "پیام شما ثبت شد" in response.content.decode()


@pytest.mark.django_db
def test_contact_email_is_optional(client, settings, mailoutbox):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    settings.CONTACT_NOTIFY_EMAIL = ""
    client.post("/fa/contact/", data=valid_form_data())
    assert mailoutbox == []


@pytest.mark.django_db
def test_contact_email_is_sent_when_configured(client, settings, mailoutbox):
    settings.CONTACT_MIN_FILL_SECONDS = 0
    settings.CONTACT_NOTIFY_EMAIL = "owner@example.com"
    client.post("/fa/contact/", data=valid_form_data())
    assert len(mailoutbox) == 1
    assert "owner@example.com" in mailoutbox[0].to


# --- بهینه‌سازی تصویر -------------------------------------------------------


def make_image_bytes(width: int, height: int, image_format: str = "JPEG") -> bytes:
    from io import BytesIO

    from PIL import Image

    buffer = BytesIO()
    Image.new("RGB", (width, height), "teal").save(buffer, format=image_format)
    return buffer.getvalue()


def test_optimize_image_resizes_large_upload():
    from io import BytesIO

    from PIL import Image

    from apps.core.uploads import MAX_IMAGE_DIMENSION, optimize_image

    optimized, (width, height) = optimize_image(BytesIO(make_image_bytes(3200, 2400)))

    assert max(width, height) <= MAX_IMAGE_DIMENSION
    assert Image.open(optimized).format == "JPEG"
    assert optimized.getbuffer().nbytes > 0


def test_optimize_image_keeps_the_original_format():
    from io import BytesIO

    from PIL import Image

    from apps.core.uploads import optimize_image

    optimized, _ = optimize_image(BytesIO(make_image_bytes(600, 400, "PNG")))
    assert Image.open(optimized).format == "PNG"


@pytest.mark.django_db
def test_service_image_is_optimized_on_save(settings, tmp_path):
    from django.core.files.uploadedfile import SimpleUploadedFile

    settings.MEDIA_ROOT = tmp_path
    upload = SimpleUploadedFile("big.jpg", make_image_bytes(3000, 2000), content_type="image/jpeg")

    service = Service(slug="with-image", title_en="With image", title_fa="با تصویر", image=upload)
    service.save()

    assert service.image_width == 2000
    assert service.image_height <= 2000
    assert service.image.name.endswith(".jpg")

    stored_name = service.image.name
    service.title_fa = "تغییر عنوان"
    service.save()
    assert service.image.name == stored_name


@pytest.mark.django_db
def test_image_derivatives_are_created(settings, tmp_path):
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    from apps.core.uploads import CARD_SIZE, THUMB_SIZE, variant_name

    settings.MEDIA_ROOT = tmp_path
    service = Service(
        slug="derivatives",
        title_en="Derivatives",
        title_fa="مشتق‌ها",
        image=SimpleUploadedFile(
            "photo.jpg", make_image_bytes(3000, 2000), content_type="image/jpeg"
        ),
    )
    service.save()

    for kind, expected in (("card", CARD_SIZE), ("thumb", THUMB_SIZE)):
        stored = variant_name(service.image.name, kind)
        assert service.image.storage.exists(stored)
        with service.image.storage.open(stored) as handle:
            assert Image.open(handle).size == expected


@pytest.mark.django_db
def test_image_variant_falls_back_to_the_original(settings, tmp_path):
    from django.core.files.uploadedfile import SimpleUploadedFile

    from apps.core.uploads import image_variant, variant_name

    settings.MEDIA_ROOT = tmp_path
    service = Service(
        slug="no-derivatives",
        title_en="No derivatives",
        title_fa="بدون مشتق",
        image=SimpleUploadedFile(
            "photo.jpg", make_image_bytes(3000, 2000), content_type="image/jpeg"
        ),
    )
    service.save()

    for kind in ("card", "thumb"):
        service.image.storage.delete(variant_name(service.image.name, kind))

    fallback = image_variant(service.image, "thumb")
    assert fallback.url == service.image.url
    assert fallback.width == service.image_width
    assert fallback.height == service.image_height


def test_image_size_validator_rejects_large_files():
    from django.core.exceptions import ValidationError
    from django.core.files.uploadedfile import SimpleUploadedFile

    from apps.core.uploads import ImageFileSizeValidator

    validator = ImageFileSizeValidator(max_bytes=10)
    with pytest.raises(ValidationError):
        validator(SimpleUploadedFile("x.jpg", b"0123456789abcdef"))


@pytest.mark.django_db
def test_contact_page_shows_the_language_specific_settings(client):
    from apps.core.models import SiteSettings

    site = SiteSettings.load()
    site.address_en = "EN ADDRESS"
    site.address_fa = "FA ADDRESS"
    site.save()

    persian = client.get("/fa/contact/").content.decode()
    english = client.get("/contact/").content.decode()

    assert "FA ADDRESS" in persian and "EN ADDRESS" not in persian
    assert "EN ADDRESS" in english
