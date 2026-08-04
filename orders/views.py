from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = (
        CartItem.objects
        .select_related("Product")
        .filter(customer=request.user)
    )

    if not cart_items.exists():
        return render(
            request,
            "cart.html",
            {
                "cart_items": cart_items,
                "total": 0,
                "message": "Your cart is empty.",
            },
        )

    total = sum(
        item.Product.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":
        order = Order.objects.create(
            customer=request.user,
            total_amount=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.Product,
                quantity=item.quantity,
                price=item.Product.price,
            )

        cart_items.delete()

        return redirect("payments:payment_page")

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )
