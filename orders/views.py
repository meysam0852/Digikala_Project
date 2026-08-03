from django.http import JsonResponse
from django.contrib.auth.models import User

from cart.models import CartItem
from .models import Order, OrderItem


def checkout(request):

    user = User.objects.first()

    cart_items = CartItem.objects.filter(customer=user)

    if not cart_items.exists():
        return JsonResponse({
            "message": "Cart is empty"
        })

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        customer=user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return JsonResponse({
        "message": "Checkout successful",
        "order_id": order.id
    })
