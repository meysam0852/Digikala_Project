from django.urls import path
from . import views


urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    path(
        "",
        views.order_list,
        name="order-list"
    ),


    path(
        "<int:id>/",
        views.order_detail,
        name="order-detail"
    ),

]