"""نمای‌های پنل مدیریت اختصاصی تماکار.

پنل جایگزین رابط پیش‌فرض جنگو است: همان مدل‌ها، اما با طراحی و مسیر خودش.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from apps.contact.models import ContactMessage
from apps.core.models import Partner, SiteImage, SiteSettings, SocialLink
from apps.services.gallery import ServiceImage
from apps.services.models import Service

from .forms import ImageForm, PartnerForm, ServiceForm, SettingsForm, SocialForm

IMAGE_KEYS = (
    ("logo", "لوگو"),
    ("home_about", "تصویر «ما کی هستیم»"),
    ("about", "تصویر صفحهٔ معرفی"),
    ("services", "تصویر صفحهٔ خدمات"),
    ("contact", "تصویر صفحهٔ تماس"),
)


class PanelLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("dashboard:index")


class PanelLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")


class PanelPasswordView(PasswordChangeView):
    template_name = "dashboard/password.html"
    success_url = reverse_lazy("dashboard:index")

    def form_valid(self, form):
        messages.success(self.request, "رمز عبور تغییر کرد.")
        return super().form_valid(form)


def panel_required(view):
    """فقط اعضای ستاد؛ بقیه به ورود پنل هدایت می‌شوند."""

    @login_required(login_url=reverse_lazy("dashboard:login"))
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return view(request, *args, **kwargs)

    return inner


@panel_required
def index(request):
    settings_obj = SiteSettings.load()
    context = {
        "active": "dashboard",
        "settings_obj": settings_obj,
        "services_count": Service.objects.count(),
        "active_services": Service.objects.filter(is_active=True).count(),
        "partners_count": Partner.objects.filter(is_active=True).count(),
        "images_count": SiteImage.objects.count(),
        "new_messages": ContactMessage.objects.filter(status="new").count(),
        "messages": ContactMessage.objects.select_related()[:6],
    }
    return render(request, "dashboard/index.html", context)


@panel_required
def settings_view(request):
    obj = SiteSettings.load()
    form = SettingsForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:settings")
    return render(request, "dashboard/settings.html", {"active": "settings", "form": form, "obj": obj})


@panel_required
def services_view(request):
    return render(
        request,
        "dashboard/services.html",
        {"active": "services", "services": Service.objects.all()},
    )


@panel_required
def service_edit(request, pk=None):
    from apps.dashboard.forms import GalleryUploadForm

    instance = get_object_or_404(Service, pk=pk) if pk else None
    form = ServiceForm(request.POST or None, request.FILES or None, instance=instance)
    gallery_form = GalleryUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        service = form.save()
        for photo in request.FILES.getlist("photos"):
            ServiceImage.objects.create(service=service, image=photo)
        return redirect("dashboard:services")
    return render(
        request,
        "dashboard/service_form.html",
        {"active": "services", "form": form, "gallery_form": gallery_form,
         "gallery": instance.gallery.all() if instance else []},
    )


@panel_required
def images_view(request):
    if request.method == "POST":
        key = request.POST.get("key", "")
        if key not in dict(IMAGE_KEYS):
            raise Http404
        obj, _ = SiteImage.objects.get_or_create(key=key)
        form = ImageForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("dashboard:images")
    else:
        form = None

    rows = []
    for key, label in IMAGE_KEYS:
        obj = SiteImage.objects.filter(key=key).first()
        rows.append({"key": key, "label": label, "obj": obj, "form": ImageForm(instance=obj)})
    return render(request, "dashboard/images.html", {"active": "images", "rows": rows})


@panel_required
def partners_view(request):
    form = PartnerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:partners")
    return render(
        request,
        "dashboard/partners.html",
        {
            "active": "partners",
            "form": form,
            "partners": Partner.objects.all(),
        },
    )


@panel_required
@require_POST
def partner_delete(request, pk):
    get_object_or_404(Partner, pk=pk).delete()
    return redirect("dashboard:partners")


@panel_required
def messages_view(request):
    return render(
        request,
        "dashboard/messages.html",
        {"active": "messages", "messages": ContactMessage.objects.all()},
    )


@panel_required
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if message.status == "new":
        message.status = "read"
        message.save(update_fields=["status", "updated_at"])
    return render(request, "dashboard/message_detail.html", {"active": "messages", "message": message})


@panel_required
def social_view(request):
    form = SocialForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:social")
    return render(
        request,
        "dashboard/social.html",
        {"active": "social", "form": form, "links": SocialLink.objects.all()},
    )
