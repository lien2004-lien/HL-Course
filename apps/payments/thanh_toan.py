import base64
from io import BytesIO

from django.http import request
import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone



from apps.courses.phan_lop import assign_enrollment_to_class

from .models import Payment


@login_required
def thanh_toan(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        student=request.user,
    )

    # =========================
    # XÁC NHẬN THANH TOÁN DEMO
    # =========================
    if request.method == "POST":

     if payment.status != Payment.Status.PAID:

        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "paid_at",
            ]
        )

        # Tự động xếp lớp sau khi thanh toán
        assign_enrollment_to_class(
            payment.enrollment
        )

        return redirect(
        "payments:payment_detail",
        payment_id=payment.id,
    )

    # =========================
    # TẠO QR
    # =========================

    qr_data = (
        f"HL-Course|"
        f"Student:{payment.student.username}|"
        f"Course:{payment.course.title}|"
        f"Amount:{payment.amount}"
    )

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return render(
        request,
        "payments/payment.html",
        {
            "payment": payment,
            "qr_code": qr_code,
        },
    )