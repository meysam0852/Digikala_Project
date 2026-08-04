from django.urls import path
from . import views

urlpatterns = [
    path("", views.store_list, name="store-list"),
    path("<int:id>/", views.store_detail, name="store-detail"),
    path("create/", views.create_store, name="create-store"),
    path("<int:id>/update/", views.update_store, name="update-store"),
    path("<int:id>/delete/", views.delete_store, name="delete-store"),
]