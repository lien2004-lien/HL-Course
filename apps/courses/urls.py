from django.urls import path

from .danh_sach_khoa_hoc import course_list
from .chi_tiet_khoa_hoc import course_detail
from .dang_ky_khoa_hoc import enroll_course


app_name = "courses"


urlpatterns = [
    path("", course_list, name="course_list"),
    path("<int:course_id>/", course_detail, name="course_detail"),
    path(
        "<int:course_id>/enroll/",
        enroll_course,
        name="enroll_course",
    ),
]