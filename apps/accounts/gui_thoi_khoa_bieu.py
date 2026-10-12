
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.courses.models import CourseClass
from apps.payments.models import Payment
from apps.notifications.models import Notification


@login_required
@require_POST
def send_class_schedule(request, class_id):

    if request.user.role != "teacher":
        raise PermissionDenied(
            "Chỉ giảng viên được gửi thời khóa biểu."
        )

    class_group = get_object_or_404(
        CourseClass,
        id=class_id,
        teacher=request.user,
        is_active=True,
    )

    schedules = list(
        class_group.schedules.all().order_by(
            "day_of_week",
            "start_time",
        )
    )

    if not schedules:
        messages.warning(
            request,
            "Lớp chưa có thời khóa biểu do Admin tạo."
        )
        return redirect("accounts:teacher_dashboard")

    students = list(
        class_group.enrollments.filter(
            payment__status=Payment.Status.PAID
        ).values_list("student_id", flat=True)
    )

    if not students:
        messages.warning(
            request,
            "Lớp chưa có học viên đã thanh toán."
        )
        return redirect("accounts:teacher_dashboard")

    schedule_lines = []

    for schedule in schedules:
        line = (
            f"{schedule.day_of_week}: "
            f"{schedule.start_time.strftime('%H:%M')} - "
            f"{schedule.end_time.strftime('%H:%M')}"
        )

        if schedule.room:
            line += f" | Phòng: {schedule.room}"

        if schedule.note:
            line += f" | Ghi chú: {schedule.note}"

        schedule_lines.append(line)

    content = (
        f"Thời khóa biểu lớp {class_group.name}\n"
        f"Khóa học: {class_group.course.title}\n\n"
        + "\n".join(schedule_lines)
    )

    with transaction.atomic():

        Notification.objects.bulk_create([
            Notification(
                recipient_id=student_id,
                sender=request.user,
                class_group=class_group,
                title="Thông báo thời khóa biểu",
                message=content,
            )
            for student_id in students
        ])

    messages.success(
        request,
        f"Đã gửi thời khóa biểu cho {len(students)} học viên."
    )

    return redirect("accounts:teacher_dashboard")
