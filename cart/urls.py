from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list, name="cart-list"),
    path("add/", views.add_to_cart, name="add-cart"),
    path("<int:id>/update/", views.update_cart, name="update-cart"),
    path("<int:id>/remove/", views.remove_from_cart, name="remove-cart"),
    path("clear/", views.clear_cart, name="clear-cart"),
]