from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import Store
from products.models import Product

def store_list(request):
    stores = Store.objects.select_related("owner").all().order_by("-id")
    return render(request, "stores.html", {"stores": stores})


def store_detail(request, id):
    store = get_object_or_404(Store.objects.select_related("owner"), id=id)
    return render(request, "store_detail.html", {"store": store})


@login_required
def create_store(request):
    if request.method == "GET":
        return render(request, "store_create.html")

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    name = (request.POST.get("name") or "").strip()
    description = (request.POST.get("description") or "").strip()

    if not name:
        messages.error(request, "Store name is required.")
        return redirect("stores:store-list")  # یا همون صفحه فرم

    store = Store.objects.create(
        owner=request.user,
        name=name,
        description=description,
    )

    messages.success(request, "Store created successfully.")
    return redirect("stores:store-detail", id=store.id)


@login_required
def update_store(request, id):
    store = get_object_or_404(Store, id=id)

    
    if store.owner != request.user:
        messages.error(request, "You are not allowed to edit this store.")
        return redirect("stores:store-detail", id=store.id)

    if request.method == "GET":
        return render(request, "store_update.html", {"store": store})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    store.name = (request.POST.get("name") or store.name).strip()
    store.description = (request.POST.get("description") or store.description).strip()
    store.save()

    messages.success(request, "Store updated successfully.")
    return redirect("stores:store-detail", id=store.id)


@login_required
def delete_store(request, id):
    store = get_object_or_404(Store, id=id)

    if store.owner != request.user:
        messages.error(request, "You are not allowed to delete this store.")
        return redirect("stores:store-detail", id=store.id)

    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully.")
        return redirect("stores:store-list")

    return render(request, "store_delete_confirm.html", {"store": store})
