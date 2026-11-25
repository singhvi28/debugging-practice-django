from django.urls import path

from views import delete_resource, revoke

urlpatterns = [
    path("revoke", revoke),
    path("resources/<str:resource_id>", delete_resource),
]
