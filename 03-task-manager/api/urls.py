from django.urls import path

from api import views

urlpatterns = [
    path("projects", views.projects_collection),
    path("projects/<str:project_id>", views.get_project),
    path("projects/<str:project_id>/tasks", views.project_tasks),
    path("tasks/<str:task_id>", views.task_detail),
]
