from django.urls import path
from api import views
urlpatterns=[path("products",views.products),path("cart",views.cart),path("checkout",views.checkout),path("orders/<str:oid>",views.get_order)]
