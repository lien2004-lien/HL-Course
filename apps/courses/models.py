from django.db import models
from apps.accounts.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
    )

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


class CourseClass(models.Model):
    name = models.CharField(
        max_length=100,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="classes",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_classes",
        limit_choices_to={"role": "teacher"},
    )

    min_students = models.PositiveIntegerField(
        default=5,
    )

    max_students = models.PositiveIntegerField(
        default=10,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.course.title} - {self.name}"

    @property
    def student_count(self):
        return self.enrollments.count()

    @property
    def is_full(self):
        return self.student_count >= self.max_students


class Schedule(models.Model):
    class_group = models.ForeignKey(
        CourseClass,
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    day_of_week = models.CharField(
        max_length=20,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    room = models.CharField(
        max_length=100,
        blank=True,
    )

    note = models.TextField(
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.class_group} - "
            f"{self.day_of_week} "
            f"{self.start_time}-{self.end_time}"
        )