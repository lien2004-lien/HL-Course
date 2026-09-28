import base64
from io import BytesIO

import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Payment


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        student=request.user,
    )

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