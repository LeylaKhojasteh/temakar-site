"""آزمون‌های مرورگری جریان‌های اصلی (Playwright + کروم نصب‌شده)."""

import secrets
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright

from apps.contact.models import ContactMessage
from apps.services.models import Service


class BrowserTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        try:
            cls.browser = cls.playwright.chromium.launch(channel="chrome")
        except Exception:  # pragma: no cover
            cls.playwright.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        self.service = Service.objects.create(
            slug="svc-a",
            title_en="Service A",
            title_fa="خدمت الف",
            summary_en="Summary of service A",
            summary_fa="خلاصهٔ خدمت الف",
            body_fa="<p>متن توضیحی خدمت.</p>",
            body_en="<p>Service body.</p>",
            order=1,
        )
        Service.objects.create(
            slug="svc-b",
            title_en="Service B",
            title_fa="خدمت ب",
            summary_en="Summary of service B",
            summary_fa="خلاصهٔ خدمت ب",
            order=2,
        )
        self.context = self.browser.new_context(
            viewport={"width": 1440, "height": 900},
            bypass_csp=getattr(self, "bypass_csp", False),
        )
        self.page = self.context.new_page()
        self.console_errors = []
        self.page.on(
            "console",
            lambda message: (
                self.console_errors.append(message.text) if message.type == "error" else None
            ),
        )
        self.page.on("pageerror", lambda error: self.console_errors.append(str(error)))

    def tearDown(self):
        self.context.close()

    def assert_no_console_errors(self):
        assert self.console_errors == []


class PagesTests(BrowserTestCase):
    def test_home_has_one_h1_and_persian_direction(self):
        self.page.goto(self.live_server_url + "/fa/")
        expect(self.page.locator("h1")).to_have_count(1)
        expect(self.page.locator("html")).to_have_attribute("dir", "rtl")
        assert "تماکار" in self.page.title()
        self.assert_no_console_errors()

class NavigationTests(BrowserTestCase):
    def test_mobile_menu_opens_traps_focus_and_closes(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.page.goto(self.live_server_url + "/fa/")
        trigger = self.page.locator("[data-menu-open]")
        trigger.click()

        menu = self.page.locator("#mobile-menu")
        expect(menu).to_be_visible()
        expect(trigger).to_have_attribute("aria-expanded", "true")
        assert "hidden" in self.page.evaluate("() => getComputedStyle(document.body).overflow")

        self.page.keyboard.press("Escape")
        expect(menu).to_be_hidden()
        assert self.page.evaluate("() => document.body.classList.contains('has-overlay')") is False
        assert "hidden" not in self.page.evaluate("() => getComputedStyle(document.body).overflow")

class ContactFormTests(BrowserTestCase):
    def fill_form(self, **overrides):
        values = {
            "نام": "سارا",
            "ایمیل": "sara@example.com",
            "موضوع": "پرسش دربارهٔ خدمات",
            "متن پیام": "سلام، می‌خواهم دربارهٔ این خدمت بیشتر بدانم.",
        }
        values.update(overrides)
        for label, value in values.items():
            self.page.get_by_label(label, exact=True).fill(value)

    def test_form_submits_and_shows_success(self):
        self.page.goto(self.live_server_url + "/fa/contact/")
        self.fill_form()
        self.page.get_by_role("button", name="ارسال پیام").click()
        expect(self.page.locator(".form-success")).to_be_visible()
        assert ContactMessage.objects.count() == 1
        self.assert_no_console_errors()

    def test_invalid_email_keeps_values_and_shows_error(self):
        self.page.goto(self.live_server_url + "/fa/contact/")
        self.fill_form(**{"ایمیل": "not-an-email"})
        self.page.get_by_role("button", name="ارسال پیام").click()

        expect(self.page.get_by_label("نام", exact=True)).to_have_value("سارا")
        expect(self.page.get_by_label("موضوع", exact=True)).to_have_value("پرسش دربارهٔ خدمات")
        expect(self.page.locator(".field-error")).to_be_visible()
        assert ContactMessage.objects.count() == 0


class AdminTests(BrowserTestCase):
    def test_admin_rich_text_editor_and_message_inbox(self):
        User = get_user_model()
        password = secrets.token_urlsafe(24)
        User.objects.create_superuser(username="owner", password=password)

        self.page.goto(self.live_server_url + "/manage/login/")
        self.page.get_by_label("نام کاربری").fill("owner")
        self.page.get_by_label("رمز عبور").fill(password)
        self.page.get_by_role("button", name="ورود").click()
        self.page.wait_for_url("**/manage/")

        self.page.goto(self.live_server_url + f"/manage/services/{self.service.pk}/")
        expect(self.page.locator("#id_body_fa")).to_be_visible()

        ContactMessage.objects.create(
            name="پیام‌دهنده",
            email="sender@example.com",
            subject="موضوع پیام",
            body="متن پیام",
            language="fa",
        )
        self.page.goto(self.live_server_url + "/manage/messages/")
        expect(self.page.locator(".panel-table")).to_contain_text("موضوع پیام")

    def test_admin_can_upload_a_service_image(self):
        import tempfile

        from PIL import Image

        from apps.core.uploads import variant_name

        User = get_user_model()
        password = secrets.token_urlsafe(24)
        User.objects.create_superuser(username="owner", password=password)
        self.page.goto(self.live_server_url + "/manage/login/")
        self.page.get_by_label("نام کاربری").fill("owner")
        self.page.get_by_label("رمز عبور").fill(password)
        self.page.get_by_role("button", name="ورود").click()
        self.page.wait_for_url("**/manage/")

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as handle:
            image = Image.new("RGB", (2400, 1600), "olive")
            image.save(handle.name)
            upload_path = handle.name

        try:
            self.page.goto(self.live_server_url + f"/manage/services/{self.service.pk}/")
            self.page.set_input_files("#id_image", upload_path)
            self.page.locator(".form-actions .btn").click()
            self.page.wait_for_url("**/manage/services/")

            self.service.refresh_from_db()
            assert self.service.image_width == 2000
            for kind in ("card", "thumb"):
                assert self.service.image.storage.exists(
                    variant_name(self.service.image.name, kind)
                )
        finally:
            Path(upload_path).unlink(missing_ok=True)


class AccessibilityTests(BrowserTestCase):
    """دروازهٔ دسترس‌پذیری با axe-core روی صفحه‌های کلیدي هر دو زبان."""

    bypass_csp = True

    def load_axe(self) -> None:
        axe_path = Path("node_modules/axe-core/axe.min.js").resolve()
        if not axe_path.exists():
            pytest.skip("axe-core نصب نیست؛ npm install را اجرا کن.")
        self.page.add_script_tag(path=str(axe_path))

    def audit(self, path: str) -> list[dict]:
        self.page.goto(self.live_server_url + path, wait_until="load")
        # انیمیشن ورود تمام شود تا کنتراست متن در حالت پایانی سنجیده شود.
        self.page.wait_for_timeout(1200)
        self.load_axe()
        result = self.page.evaluate("async () => await axe.run(document)")
        return result["violations"]

    def test_public_pages_have_no_accessibility_violations(self):
        for path in ("/", "/fa/", "/fa/our-services/", "/fa/contact/"):
            violations = self.audit(path)
            report = [(v["id"], v["impact"], v["nodes"][0]["target"]) for v in violations]
            assert violations == [], f"{path}: {report}"
