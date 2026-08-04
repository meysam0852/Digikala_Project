from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Product
from stores.models import Store


# ==========================
# GET ALL PRODUCTS
# ==========================

def product_list(request):
    products = list(
        Product.objects.values(
            "id",
            "name",
            "description",
            "price",
            "image",
            "store__id",
            "store__name",
        )
    )

    return JsonResponse(products, safe=False)


# ==========================
# GET SINGLE PRODUCT
# ==========================

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "image": product.image.url if product.image else None,
        "store": {
            "id": product.store.id,
            "name": product.store.name,
        }
    })


# ==========================
# CREATE PRODUCT
# ==========================

@require_http_methods(["POST"])
def create_product(request):

    store_id = request.POST.get("store_id")

    store = get_object_or_404(Store, id=store_id)

    product = Product.objects.create(
        store=store,
        name=request.POST.get("name"),
        description=request.POST.get("description"),
        price=request.POST.get("price"),
        image=request.FILES.get("image")
    )

    return JsonResponse({
        "message": "Product created successfully",
        "product_id": product.id
    })


# ==========================
# UPDATE PRODUCT
# ==========================

@require_http_methods(["POST"])
def update_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.POST.get("name"):
        product.name = request.POST.get("name")

    if request.POST.get("description"):
        product.description = request.POST.get("description")

    if request.POST.get("price"):
        product.price = request.POST.get("price")

    if request.FILES.get("image"):
        product.image = request.FILES.get("image")

    product.save()

    return JsonResponse({
        "message": "Product updated successfully"
    })


# ==========================
# DELETE PRODUCT
# ==========================

@require_http_methods(["POST"])
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    product.delete()

    return JsonResponse({
        "message": "Product deleted successfully"
    })