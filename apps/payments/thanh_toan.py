import base64
from io import BytesIO

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

    # ==========================
    # THÔNG TIN THANH TOÁN DEMO
    # ==========================

    bank_name = "MB Bank"
    bank_account = "0123456789"
    account_name = "HL COURSE"

    transfer_content = f"HLCOURSE-PAY-{payment.id}"

    # ==========================
    # XÁC NHẬN THANH TOÁN DEMO
    # ==========================

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

            # Thanh toán thành công
            # -> tự động phân lớp
            assign_enrollment_to_class(
                payment.enrollment
            )

        return redirect(
            "payments:payment_detail",
            payment_id=payment.id,
        )

    # ==========================
    # DỮ LIỆU QR
    # ==========================

    qr_data = (
        f"HL COURSE PAYMENT\n"
        f"Payment ID: {payment.id}\n"
        f"Bank: {bank_name}\n"
        f"Account: {bank_account}\n"
        f"Account Name: {account_name}\n"
        f"Student: {payment.student.username}\n"
        f"Course: {payment.course.title}\n"
        f"Amount: {payment.amount}\n"
        f"Content: {transfer_content}"
    )

    qr = qrcode.make(qr_data)

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return render(
        request,
        "payments/payment.html",
        {
            "payment": payment,
            "qr_code": qr_code,

            "bank_name": bank_name,
            "bank_account": bank_account,
            "account_name": account_name,
            "transfer_content": transfer_content,
        },
    )