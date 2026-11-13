"""صفحه‌های خطا با تنظیمات تولیدی رندر می‌شوند.

در حالت DEBUG، جنگو صفحهٔ فنی خودش را نشان می‌دهد؛ پس این تست مستقیم handlerها را
صدا می‌زند تا مطمئن شویم قالب طراحی‌شده سالم است.
"""

import pytest
from django.test import RequestFactory

from apps.core.views import page_not_found, server_error


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.mark.django_db
def test_404_handler_renders_designed_page(request_factory):
    response = page_not_found(request_factory.get("/missing/"))
    body = response.content.decode()

    assert response.status_code == 404
    assert 'class="error-code"' in body
    assert "page-title" in body
    assert "<header" in body and "<footer" in body


@pytest.mark.django_db
def test_500_handler_renders_designed_page(request_factory):
    response = server_error(request_factory.get("/boom/"))
    body = response.content.decode()

    assert response.status_code == 500
    assert 'class="error-code"' in body
    assert "500" in body
