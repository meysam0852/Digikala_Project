from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render


@login_required
def payment_page(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        if amount:
            try:
                amount = int(amount)

                if amount > 0:
                    with transaction.atomic():
                        profile = request.user.customer_profile
                        profile.balance += amount
                        profile.save()

                    messages.success(
                        request,
                        f"موجودی شما به میزان {amount:,} تومان افزایش یافت."
                    )

                    return redirect("payments:payment_page")

                messages.error(request, "مبلغ باید بیشتر از صفر باشد.")

            except ValueError:
                messages.error(request, "مبلغ وارد شده معتبر نیست.")

            except AttributeError:
                messages.error(
                    request,
                    "برای این کاربر پروفایل مشتری وجود ندارد."
                )

    return render(request, "payment.html")
