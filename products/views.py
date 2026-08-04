from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from stores.models import Store


def home_view(request):
    products = Product.objects.select_related("store").all()

    return render(
        request,
        "home.html",
        {
            "products": products,
        },
    )




def product_list(request):
    products = Product.objects.select_related("store").all()

    return render(
        request,
        "home.html",
        {
            "products": products,
        },
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "store": product.store.name if product.store else None,
    })

def create_product(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    store = Store.objects.first()

    product = Product.objects.create(
        store=store,
        name=request.POST.get("name"),
        description=request.POST.get("description"),
        price=request.POST.get("price"),
    )

    return JsonResponse({
        "message": "Product created successfully",
        "id": product.id,
    })


def update_product(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    product = get_object_or_404(Product, id=id)

    product.name = request.POST.get("name", product.name)
    product.description = request.POST.get("description", product.description)
    product.price = request.POST.get("price", product.price)

    product.save()

    return JsonResponse({
        "message": "Product updated successfully"
    })


def delete_product(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    product = get_object_or_404(Product, id=id)

    product.delete()

    return JsonResponse({
        "message": "Product deleted successfully"
    })
