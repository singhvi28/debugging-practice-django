from django.urls import path

from views import count_users, create_user

urlpatterns = [
    path("register", create_user),
    path("users/count", count_users),
]
