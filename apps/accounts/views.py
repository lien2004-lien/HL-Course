from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Đăng ký tài khoản thành công."
            )

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


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


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("home")

    return render(
        request,
        "accounts/student_dashboard.html"
    )


@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        return redirect("home")

    return render(
        request,
        "accounts/teacher_dashboard.html"
    )


