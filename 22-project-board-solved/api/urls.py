from django.urls import path
from api import views
urlpatterns=[path('projects',views.projects),path('projects/<str:pid>/archive',views.archive),path('projects/<str:pid>/tasks',views.tasks),path('tasks',views.task_list),path('tasks/<str:tid>',views.update)]
