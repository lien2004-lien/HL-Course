from django.db import models
from apps.accounts.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "teacher"},
        related_name="courses",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title