from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import CartItem
from products.models import Product
from django.contrib.auth.models import User


# ==========================
# VIEW CART
# ==========================

def cart_list(request):

    user = User.objects.first()

    cart = CartItem.objects.filter(customer=user)

    data = []

    total = 0

    for item in cart:

        subtotal = item.product.price * item.quantity
        total += subtotal

        data.append({
            "id": item.id,
            "product": item.product.name,
            "price": str(item.product.price),
            "quantity": item.quantity,
            "subtotal": str(subtotal),
        })

    return JsonResponse({
        "items": data,
        "total": str(total)
    })


# ==========================
# ADD TO CART
# ==========================
@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):

    user = User.objects.first()

    product = get_object_or_404(
        Product,
        id=request.POST.get("product_id")
    )

    cart_item, created = CartItem.objects.get_or_create(
        customer=user,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        "message": "Product added to cart."
    })


# ==========================
# UPDATE QUANTITY
# ==========================
@csrf_exempt
@require_http_methods(["POST"])
def update_cart(request, id):

    cart_item = get_object_or_404(CartItem, id=id)

    quantity = int(request.POST.get("quantity"))

    if quantity <= 0:
        cart_item.delete()

        return JsonResponse({
            "message": "Item removed."
        })

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        "message": "Cart updated."
    })


# ==========================
# REMOVE ITEM
# ==========================
@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request, id):

    cart_item = get_object_or_404(CartItem, id=id)

    cart_item.delete()

    return JsonResponse({
        "message": "Item removed successfully."
    })


# ==========================
# CLEAR CART
# ==========================
@csrf_exempt
@require_http_methods(["POST"])
def clear_cart(request):

    user = User.objects.first()

    CartItem.objects.filter(customer=user).delete()

    return JsonResponse({
        "message": "Cart cleared successfully."
    })