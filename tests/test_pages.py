import pytest
from django.urls import reverse

from .test_core import make_service




@pytest.mark.django_db
def test_persian_page_falls_back_to_the_english_body(client):
    service = make_service(slug="english-only", body_fa="", body_en="<p>English body only.</p>")

    response = client.get(f"/fa/our-services/{service.slug}/")

    assert response.status_code == 200
    assert "English body only" in response.content.decode()


@pytest.mark.django_db
def test_detail_page_builds_a_section_index(client):
    service = make_service(
        slug="with-sections",
        body_fa="<p>مقدمه</p><h3>کشنده‌ها</h3><p>متن</p><h3>تنظیم‌کشش‌ها</h3><p>متن</p>",
    )

    response = client.get(f"/fa/our-services/{service.slug}/")

    assert [item["label"] for item in response.context["toc"]] == ["کشنده‌ها", "تنظیم‌کشش‌ها"]
    body = response.content.decode()
    assert 'id="section-1"' in body
    assert 'href="#section-1"' in body
    assert 'id="section-2"' in body


@pytest.mark.django_db
def test_detail_without_headings_has_no_index(client):
    service = make_service(slug="no-sections", body_fa="<p>فقط یک پاراگراف.</p>")

    response = client.get(f"/fa/our-services/{service.slug}/")

    assert response.context["toc"] == []
    assert "در این صفحه" not in response.content.decode()
