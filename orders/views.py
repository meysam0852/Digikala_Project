from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Order, OrderItem
from cart.models import CartItem



# ==========================
# CHECKOUT
# ==========================
@csrf_exempt
@require_http_methods(["POST"])
def checkout(request):

    user = User.objects.first()

    cart_items = CartItem.objects.filter(
        customer=user
    )


    if not cart_items.exists():
        return JsonResponse({
            "error": "Cart is empty"
        }, status=400)



    total_amount = 0


    # محاسبه مبلغ کل
    for item in cart_items:
        total_amount += item.product.price * item.quantity



    # ساخت Order

    order = Order.objects.create(
        customer=user,
        total_amount=total_amount
    )


    # ساخت Order Items

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )



    # خالی کردن سبد

    cart_items.delete()



    return JsonResponse({
        "message": "Order created successfully",
        "order_id": order.id,
        "total": str(order.total_amount)
    })




# ==========================
# ORDER LIST
# ==========================

def order_list(request):

    user = User.objects.first()

    orders = Order.objects.filter(
        customer=user
    )


    data = []


    for order in orders:

        data.append({
            "id": order.id,
            "total_amount": str(order.total_amount),
            "created_at": order.created_at
        })


    return JsonResponse(data, safe=False)




# ==========================
# ORDER DETAIL
# ==========================

def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )


    items = []


    for item in order.items.all():

        items.append({
            "product": item.product.name,
            "quantity": item.quantity,
            "price": str(item.price)
        })



    return JsonResponse({

        "id": order.id,

        "customer": order.customer.username,

        "total_amount": str(order.total_amount),

        "items": items,

        "created_at": order.created_at

    })