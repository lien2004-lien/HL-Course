
from django.urls import path

from .danh_sach_thong_bao import student_notifications

from .danh_dau_da_doc import (
    mark_notification_read,
    mark_all_notifications_read,
)


app_name = "notifications"


urlpatterns = [
    path(
        "",
        student_notifications,
        name="student_notifications",
    ),

    path(
        "<int:notification_id>/read/",
        mark_notification_read,
        name="mark_notification_read",
    ),

    path(
        "read-all/",
        mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
]
