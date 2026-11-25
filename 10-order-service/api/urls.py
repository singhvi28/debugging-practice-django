from django.urls import path

from api import views

urlpatterns = [
    path("products", views.list_products),
    path("products/<str:product_id>", views.get_product),
    path("orders", views.create_order),
    path("orders/<str:order_id>", views.order_detail),
    path("orders/<str:order_id>/status", views.update_order_status),
]
