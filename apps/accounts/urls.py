from django.urls import path

from .dang_ky import register_view
from .dang_nhap import login_view
from .dang_xuat import logout_view
from .hoc_vien import student_dashboard
from .giang_vien import teacher_dashboard

from .xuat_danh_sach_lop import export_class_students

from .gui_thoi_khoa_bieu import send_class_schedule


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

    path(
    "teacher/classes/<int:class_id>/export/",
    export_class_students,
    name="export_class_students",
    ),

    path(
    "teacher/classes/<int:class_id>/send-schedule/",
    send_class_schedule,
    name="send_class_schedule",
    ),
]