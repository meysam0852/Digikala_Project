from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("<int:id>/", views.product_detail, name="product-detail"),
    path("create/", views.create_product, name="product-create"),
    path("<int:id>/update/", views.update_product, name="product-update"),
    path("<int:id>/delete/", views.delete_product, name="product-delete"),
]