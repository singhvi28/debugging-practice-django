from django.urls import path
from api import views
urlpatterns=[path('expenses',views.create),path('expenses/total',views.total),path('expenses/<str:i>',views.detail),path('expenses/<str:i>/decision',views.decide)]
