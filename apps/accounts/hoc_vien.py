from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.payments.models import Payment


@login_required
def student_dashboard(request):

    # Chỉ học viên mới được vào trang này
    if request.user.role != "student":
        return redirect("home")

    # Các khóa học đang mở để học viên đăng ký
    courses = Course.objects.filter(
        is_active=True
    )

    # Chỉ lấy khóa học đã thanh toán
    my_enrollments = Enrollment.objects.filter(
        student=request.user,
        payment__status=Payment.Status.PAID,
    ).select_related(
        "course",
    )

    return render(
        request,
        "accounts/student_dashboard.html",
        {
            "courses": courses,
            "my_enrollments": my_enrollments,
        },
    )