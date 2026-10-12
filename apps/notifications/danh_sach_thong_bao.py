
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from .models import Notification


@login_required
def student_notifications(request):

    if request.user.role != "student":
        raise PermissionDenied(
            "Chỉ học viên được xem thông báo."
        )

    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related(
            "sender",
            "class_group",
        )
        .order_by("-created_at")
    )

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        "notifications/student_notifications.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )
