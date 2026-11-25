from django.urls import path

from views import enriched_orders

urlpatterns = [
    path("orders/enriched", enriched_orders),
]
