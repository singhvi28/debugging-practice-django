from django.urls import path

from views import item_detail

urlpatterns = [
    path("items/<str:item_id>", item_detail),
]
