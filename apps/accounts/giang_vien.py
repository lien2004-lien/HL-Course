from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.courses.models import CourseClass


@login_required
def teacher_dashboard(request):

    if request.user.role != "teacher":
        return redirect("home")

    classes = (
        CourseClass.objects
        .filter(
            teacher=request.user,
            is_active=True,
        )
        .select_related("course")
        .prefetch_related(
            "enrollments__student",
            "schedules",
        )
        .order_by("course__title", "name")
    )

    total_classes = classes.count()

    total_students = sum(
        class_group.student_count
        for class_group in classes
    )

    return render(
        request,
        "accounts/teacher_dashboard.html",
        {
            "classes": classes,
            "total_classes": total_classes,
            "total_students": total_students,
        },
    )