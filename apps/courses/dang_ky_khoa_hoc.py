from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Course
from apps.enrollments.models import Enrollment
from apps.payments.models import Payment


@login_required
def enroll_course(request, course_id):
    if request.user.role != "student":
        messages.error(
            request,
            "Chỉ học viên mới được đăng ký khóa học."
        )
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
            payment = Payment.objects.create(
                student=request.user,
                course=course,
                enrollment=enrollment,
                amount=course.price,
            )

            return redirect(
                "payments:payment_detail",
                payment_id=payment.id,
            )

        else:
            messages.warning(
                request,
                "Bạn đã đăng ký khóa học này rồi."
            )

    return redirect("accounts:student_dashboard")