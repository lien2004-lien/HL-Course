from django.shortcuts import render

from apps.accounts.models import User
from apps.courses.models import Course
from apps.enrollments.models import Enrollment


def home_view(request):
    courses = Course.objects.filter(
        is_active=True
    ).order_by("-id")[:6]

    teachers = User.objects.filter(
        role="teacher",
        is_active=True
    ).order_by("-id")[:4]

    course_count = Course.objects.filter(is_active=True).count()
    student_count = User.objects.filter(
        role="student",
        is_active=True
    ).count()
    teacher_count = User.objects.filter(
        role="teacher",
        is_active=True
    ).count()
    enrollment_count = Enrollment.objects.count()

    context = {
        "courses": courses,
        "teachers": teachers,
        "course_count": course_count,
        "student_count": student_count,
        "teacher_count": teacher_count,
        "enrollment_count": enrollment_count,
    }

    return render(request, "home.html", context)