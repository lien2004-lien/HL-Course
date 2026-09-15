from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course
from apps.enrollments.models import Enrollment


def course_list(request):
    courses = Course.objects.filter(is_active=True)

    return render(
        request,
        "courses/course_list.html",
        {"courses": courses},
    )


@login_required
def enroll_course(request, course_id):
    if request.user.role != "student":
        messages.error(request, "Chỉ học viên mới được đăng ký khóa học.")
        return redirect("courses:course_list")

    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True,
    )

    if request.method == "POST":
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
        )

        if created:
            messages.success(
                request,
                f"Đăng ký khóa học '{course.title}' thành công.",
            )
        else:
            messages.warning(
                request,
                "Bạn đã đăng ký khóa học này rồi.",
            )

    return redirect("accounts:student_dashboard")