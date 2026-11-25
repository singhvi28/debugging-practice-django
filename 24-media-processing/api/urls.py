from django.urls import path
from api import views
urlpatterns=[path('media',views.listing),path('media/<str:i>',views.media),path('media/<str:i>/process',views.process),path('media/<str:i>/signed_url',views.signed)]
