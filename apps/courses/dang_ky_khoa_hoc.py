from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Course
from apps.enrollments.models import Enrollment
from apps.payments.models import Payment


@login_required
def enroll_course(request, course_id):

    # Chỉ học viên mới được đăng ký
    if request.user.role != "student":
        messages.error(
            request,
            "Chỉ học viên mới được đăng ký khóa học."
        )
        return redirect("courses:course_list")

    # Lấy khóa học
    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True,
    )

    # Chỉ xử lý khi gửi POST
    if request.method != "POST":
        return redirect("accounts:student_dashboard")

    # Tìm hoặc tạo đăng ký
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
    )

    # Tìm Payment của Enrollment
    try:
        payment = enrollment.payment
    except Payment.DoesNotExist:
        payment = None

    # Nếu đã thanh toán
    if payment and payment.status == Payment.Status.PAID:
        messages.warning(
            request,
            "Bạn đã thanh toán khóa học này rồi."
        )
        return redirect("accounts:student_dashboard")

    # Nếu đã đăng ký nhưng chưa thanh toán
    if payment and payment.status == Payment.Status.PENDING:
        return redirect(
            "payments:payment_detail",
            payment_id=payment.id,
        )

    # Nếu chưa có Payment thì tạo mới
    payment = Payment.objects.create(
        student=request.user,
        course=course,
        enrollment=enrollment,
        amount=course.price,
    )

    # Chuyển sang trang thanh toán
    return redirect(
        "payments:payment_detail",
        payment_id=payment.id,
    )