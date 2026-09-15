from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "amount",
        "status",
        "created_at",
        "paid_at",
    )

    list_filter = (
        "status",
        "course",
    )

    search_fields = (
        "student__username",
        "student__email",
        "course__title",
    )