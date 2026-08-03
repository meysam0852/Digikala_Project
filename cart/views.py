from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import CartItem
from products.models import Product


def cart_list(request):
    user = User.objects.first()

    cart = CartItem.objects.filter(customer=user)

    data = []

    for item in cart:
        data.append({
            "id": item.id,
            "product": item.product.name,
            "price": str(item.product.price),
            "quantity": item.quantity,
        })

    return JsonResponse(data, safe=False)

def add_to_cart(request, product_id):

    user = User.objects.first()

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        customer=user,
        product=product,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        "message": "Product added to cart"
    })
    
def remove_from_cart(request, id):

    item = get_object_or_404(CartItem, id=id)

    item.delete()

    return JsonResponse({
        "message": "Item removed"
    })
