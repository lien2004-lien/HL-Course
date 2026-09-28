from django.urls import path

from .thanh_toan import payment_detail


app_name = "payments"

urlpatterns = [
    path(
        "<int:payment_id>/",
        payment_detail,
        name="payment_detail",
    ),
]