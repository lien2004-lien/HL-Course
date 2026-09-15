from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "teacher",
        "is_active",
    )

    list_filter = (
        "is_active",
        "teacher",
    )

    search_fields = (
        "title",
        "description",
    )