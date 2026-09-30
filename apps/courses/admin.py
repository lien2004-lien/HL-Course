from django.contrib import admin

from .models import Course, CourseClass, Schedule


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


@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "course",
        "teacher",
        "student_count_display",
        "min_students",
        "max_students",
        "is_active",
    )

    list_filter = (
        "course",
        "teacher",
        "is_active",
    )

    search_fields = (
        "name",
        "course__title",
        "teacher__username",
    )

    @admin.display(description="Số học viên")
    def student_count_display(self, obj):
        return obj.student_count


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "class_group",
        "day_of_week",
        "start_time",
        "end_time",
        "room",
    )

    list_filter = (
        "day_of_week",
        "class_group",
    )

    search_fields = (
        "class_group__name",
        "class_group__course__title",
        "room",
    )