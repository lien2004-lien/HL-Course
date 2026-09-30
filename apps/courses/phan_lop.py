from django.db import transaction

from .models import CourseClass


@transaction.atomic
def assign_enrollment_to_class(enrollment):

    # Nếu học viên đã được xếp lớp thì giữ nguyên
    if enrollment.class_group_id:
        return enrollment.class_group

    course = enrollment.course

    # Khóa các lớp hiện có trong lúc phân lớp
    classes = (
        CourseClass.objects
        .select_for_update()
        .filter(
            course=course,
            is_active=True,
        )
        .order_by("id")
    )

    class_group = None

    # Tìm lớp còn chỗ
    for current_class in classes:

        if current_class.student_count < current_class.max_students:
            class_group = current_class
            break

    # Nếu tất cả lớp đều đủ 10 hoặc chưa có lớp nào
    # thì tự động mở lớp mới
    if class_group is None:

        class_number = (
            CourseClass.objects
            .filter(course=course)
            .count()
            + 1
        )

        class_group = CourseClass.objects.create(
            name=f"Lớp {class_number:02d}",
            course=course,
            teacher=course.teacher,
            min_students=5,
            max_students=10,
            is_active=True,
        )

    # Xếp học viên vào lớp
    enrollment.class_group = class_group

    enrollment.save(
        update_fields=["class_group"]
    )

    return class_group