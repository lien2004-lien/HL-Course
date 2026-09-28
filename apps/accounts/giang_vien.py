from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        return redirect("home")

    return render(
        request,
        "accounts/teacher_dashboard.html"
    )