from django.urls import path

from . import thanh_toan


app_name = "payments"


urlpatterns = [
    path(
        "<int:payment_id>/",
        thanh_toan.thanh_toan,
        name="payment_detail",
    ),
]