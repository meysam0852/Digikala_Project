from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Store

import json


# ===========================
# GET ALL STORES
# ===========================

def store_list(request):
    stores = list(
        Store.objects.values(
            "id",
            "name",
            "description",
            "owner__username",
            "created_at",
        )
    )

    return JsonResponse(stores, safe=False)


# ===========================
# GET ONE STORE
# ===========================

def store_detail(request, id):
    store = get_object_or_404(Store, id=id)

    return JsonResponse({
        "id": store.id,
        "name": store.name,
        "description": store.description,
        "owner": store.owner.username,
        "created_at": store.created_at,
    })


# ===========================
# CREATE STORE
# ===========================

@require_http_methods(["POST"])
def create_store(request):

    data = json.loads(request.body)

    owner = get_object_or_404(
        User,
        id=data["owner_id"]
    )

    store = Store.objects.create(
        owner=owner,
        name=data["name"],
        description=data.get("description", "")
    )

    return JsonResponse({
        "message": "Store created successfully",
        "id": store.id
    })


# ===========================
# UPDATE STORE
# ===========================

@require_http_methods(["PUT"])
def update_store(request, id):

    store = get_object_or_404(Store, id=id)

    data = json.loads(request.body)

    store.name = data.get("name", store.name)
    store.description = data.get(
        "description",
        store.description
    )

    store.save()

    return JsonResponse({
        "message": "Store updated successfully"
    })


# ===========================
# DELETE STORE
# ===========================

@require_http_methods(["DELETE"])
def delete_store(request, id):

    store = get_object_or_404(Store, id=id)

    store.delete()

    return JsonResponse({
        "message": "Store deleted successfully"
    })