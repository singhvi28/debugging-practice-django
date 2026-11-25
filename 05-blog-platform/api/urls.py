from django.urls import path

from api import views

urlpatterns = [
    path("posts", views.posts_collection),
    path("posts/<str:post_id>", views.get_post),
    path("posts/remove/<str:post_id>", views.delete_post),
    path("posts/<str:post_id>/comments", views.post_comments),
]
