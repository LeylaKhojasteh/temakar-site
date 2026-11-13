"""ساخت مسیرهای بخش عمومی."""

from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("who-we-are/", views.who_we_are, name="who_we_are"),
]
