from django.urls import path

from api import views

urlpatterns = [
    path("products", views.products_collection),
    path("products/<str:product_id>", views.get_product),
    path("products/<str:product_id>/stock", views.adjust_stock),
    path("products/<str:product_id>/moves", views.list_moves),
]
