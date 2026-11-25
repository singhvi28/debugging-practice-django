from django.urls import path

from api import views

urlpatterns = [
    path("locations", views.list_locations),
    path("locations/<str:location_id>/stock", views.get_location_stock),
    path("locations/<str:location_id>/stock/<str:sku>", views.get_sku_stock),
    path("transfers", views.create_transfer),
    path("transfers/<str:transfer_id>", views.get_transfer),
]
