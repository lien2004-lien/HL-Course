from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse("HL Course - Trang chủ")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("courses/", include("apps.courses.urls")),
    path("", home_view, name="home"),
    path("payments/", include("apps.payments.urls")),
]