from django.contrib import admin
from django.urls import include, path

from .trang_chu import home_view


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "accounts/",
        include("apps.accounts.urls")
    ),

    path(
        "courses/",
        include("apps.courses.urls")
    ),

    path(
        "payments/",
        include("apps.payments.urls")
    ),

    path(
        "",
        home_view,
        name="home"
    ),
]