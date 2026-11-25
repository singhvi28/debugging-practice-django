from django.urls import path

from api import views

urlpatterns = [
    path("threads/deleted", views.list_deleted_threads),
    path("threads/<str:thread_id>/replies/<str:reply_id>", views.delete_reply),
    path("threads/<str:thread_id>/replies", views.create_reply),
    path("threads/<str:thread_id>", views.get_thread),
    path("threads", views.threads_collection),
]
