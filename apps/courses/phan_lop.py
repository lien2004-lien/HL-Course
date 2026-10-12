from django.db import transaction

from .models import CourseClass


@transaction.atomic
def assign_enrollment_to_class(enrollment):

    # Đã có lớp thì không phân lại
    if enrollment.class_group_id:
        return enrollment.class_group

    # Chỉ học viên đã thanh toán mới được vào lớp
    try:
        payment = enrollment.payment
    except Exception:
        return None

    if payment.status != "paid":
        return None

    course = enrollment.course

    # Tìm lớp của đúng khóa học còn chỗ
    classes = CourseClass.objects.filter(
        course=course,
        is_active=True,
    ).order_by("id")

    for class_group in classes:

        if class_group.student_count < class_group.max_students:

            enrollment.class_group = class_group

            enrollment.save(
                update_fields=[
                    "class_group"
                ]
            )

            return class_group

    # Không còn lớp nào có chỗ
    # -> tự động mở lớp mới

    class_number = (
        CourseClass.objects.filter(
            course=course
        ).count()
        + 1
    )

    class_group = CourseClass.objects.create(
        name=f"Lớp {class_number:02d}",
        course=course,
        teacher=course.teacher,
        min_students=5,
        max_students=10,
    )

    enrollment.class_group = class_group

    enrollment.save(
        update_fields=[
            "class_group"
        ]
    )

    return class_group