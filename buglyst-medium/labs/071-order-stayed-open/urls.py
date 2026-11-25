from django.urls import path

from views import admin_reset, create_order, get_inventory, get_orders, orders_endpoint

urlpatterns = [
    path("orders", orders_endpoint),
    path("inventory", get_inventory),
    path("admin/reset", admin_reset),
]
