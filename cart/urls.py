from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list, name="cart-list"),
    path("add/<int:product_id>/", views.add_to_cart, name="add-cart"),
    path("remove/<int:id>/", views.remove_from_cart, name="remove-cart"),
]