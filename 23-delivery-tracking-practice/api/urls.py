from django.urls import path
from api import views
urlpatterns=[path('shipments/<str:i>',views.detail),path('shipment/<str:i>/status',views.status),path('shipments/<str:i>/webhook',views.webhook)]
