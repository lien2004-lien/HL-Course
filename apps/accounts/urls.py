from django.urls import path

from .dang_ky import register_view
from .dang_nhap import login_view
from .dang_xuat import logout_view
from .hoc_vien import student_dashboard
from .giang_vien import teacher_dashboard


app_name = "accounts"


urlpatterns = [
    path(
        "register/",
        register_view,
        name="register",
    ),

    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),

    path(
        "student/",
        student_dashboard,
        name="student_dashboard",
    ),

    path(
        "teacher/",
        teacher_dashboard,
        name="teacher_dashboard",
    ),
]