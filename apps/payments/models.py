from django.db import models

from apps.accounts.models import User
from apps.courses.models import Course
from apps.enrollments.models import Enrollment


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Chờ thanh toán"
        PAID = "paid", "Đã thanh toán"
        CANCELLED = "cancelled", "Đã hủy"

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        limit_choices_to={"role": "student"},
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.status}"