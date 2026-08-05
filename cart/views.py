from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import CartItem


@login_required
def cart_list(request):
    cart_items = (
        CartItem.objects
        .select_related("Product", "Product__store")
        .filter(customer=request.user)
    )

    total = sum(
        item.Product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
    )

    cart_item, created = CartItem.objects.get_or_create(
        customer=request.user,
        Product=product,
        defaults={
            "quantity": 1,
        },
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

    return redirect("cart:cart-list")


@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(
        CartItem,
        id=id,
        customer=request.user,
    )

    cart_item.delete()

    return redirect("cart:cart-list")
