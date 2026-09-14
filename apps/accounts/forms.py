from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        ]

    def clean_role(self):
        role = self.cleaned_data["role"]

        if role == User.Role.ADMIN:
            raise forms.ValidationError(
                "Không được đăng ký tài khoản Admin."
            )

        return role