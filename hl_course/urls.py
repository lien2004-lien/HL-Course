from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse("HL Course - Trang chủ")

    return HttpResponse(
        'HL Course - Trang chủ<br><br>'
        '<a href="/accounts/login/">Đăng nhập</a>'
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("", home_view, name="home"),
]