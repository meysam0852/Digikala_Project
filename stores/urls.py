from django.urls import path
from . import views

urlpatterns = [

    path("", views.store_list),

    path("<int:id>/", views.store_detail),

    path("create/", views.create_store),

    path("<int:id>/update/", views.update_store),

    path("<int:id>/delete/", views.delete_store),

]

