from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Store


def store_list(request):
    stores = list(
        Store.objects.values(
            "id",
            "name",
            "description",
        )
    )

    return JsonResponse(stores, safe=False)


def store_detail(request, id):
    store = get_object_or_404(Store, id=id)

    return JsonResponse({
        "id": store.id,
        "name": store.name,
        "description": store.description,
        "owner":store.owner.username,
        "created_at":store.created_at,
        
    })
    
    
def create_store(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    user = User.objects.first() 

    store = Store.objects.create(
        owner=user,
        name=request.POST.get("name"),
        description=request.POST.get("description"),
    )

    return JsonResponse({
        "message": "Store created successfully",
        "id": store.id,
    })
    
def update_store(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    store = get_object_or_404(Store, id=id)

    store.name = request.POST.get("name", store.name)
    store.description = request.POST.get("description", store.description)
    store.save()

    return JsonResponse({
        "message": "Store updated successfully"
    })


def delete_store(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    store = get_object_or_404(Store, id=id)
    store.delete()

    return JsonResponse({
        "message": "Store deleted successfully"
    })
