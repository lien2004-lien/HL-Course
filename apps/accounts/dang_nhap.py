from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser or user.role == "admin":
                return redirect("admin:index")

            if user.role == "teacher":
                return redirect("accounts:teacher_dashboard")

            return redirect("accounts:student_dashboard")

        messages.error(
            request,
            "Tên đăng nhập hoặc mật khẩu không đúng."
        )

    return render(request, "accounts/login.html")