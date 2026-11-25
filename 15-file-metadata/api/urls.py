from django.urls import path

from api import views

urlpatterns = [
    path("api/files", views.files_collection),
    path("api/files/<str:file_id>/tags", views.add_tag),
    path("api/files/<str:file_id>", views.file_detail),
]
