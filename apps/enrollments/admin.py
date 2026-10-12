from django.contrib import admin

from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "payment_status_display",
        "class_group",
        "enrolled_at",
    )

    list_filter = (
        "course",
        "class_group",
        "enrolled_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "course__title",
        "class_group__name",
    )

    @admin.display(
        description="Thanh toán"
    )
    def payment_status_display(self, obj):

        try:
            return obj.payment.get_status_display()

        except Exception:
            return "Chưa có thanh toán"