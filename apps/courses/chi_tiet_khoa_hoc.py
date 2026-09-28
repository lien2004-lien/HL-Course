from django.shortcuts import get_object_or_404, render

from .models import Course


def course_detail(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True,
    )

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
        },
    )