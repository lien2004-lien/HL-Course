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
        "max_students",
        "class_status",
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

    @admin.display(
        description="Sĩ số"
    )
    def student_count_display(self, obj):
        return obj.student_count

    @admin.display(
        description="Trạng thái lớp"
    )
    def class_status(self, obj):

        count = obj.student_count

        if count >= obj.max_students:
            return "Đã đầy"

        if count >= obj.min_students:
            return "Đủ điều kiện mở lớp"

        return "Chưa đủ học viên"


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
        "class_group",
        "day_of_week",
    )