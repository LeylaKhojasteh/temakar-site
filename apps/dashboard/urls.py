"""مسیرهای پنل مدیریت تماکار."""

from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.PanelLoginView.as_view(), name="login"),
    path("logout/", views.PanelLogoutView.as_view(), name="logout"),
    path("password/", views.PanelPasswordView.as_view(), name="password"),
    path("", views.index, name="index"),
    path("settings/", views.settings_view, name="settings"),
    path("upload-image/", __import__("apps.dashboard.uploads", fromlist=["upload_inline_image"]).upload_inline_image, name="upload_image"),
    path("services/", views.services_view, name="services"),
    path("services/new/", views.service_edit, name="service_new"),
    path("services/<int:pk>/", views.service_edit, name="service_edit"),
    path("images/", views.images_view, name="images"),
    path("partners/", views.partners_view, name="partners"),
    path("partners/<int:pk>/delete/", views.partner_delete, name="partner_delete"),
    path("messages/", views.messages_view, name="messages"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("social/", views.social_view, name="social"),
]
