from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.courses.models import Course


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("home")

    courses = Course.objects.filter(
        is_active=True
    )

    return render(
        request,
        "accounts/student_dashboard.html",
        {"courses": courses},
    )