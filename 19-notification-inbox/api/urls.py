from django.urls import path

from api import views

urlpatterns = [
    path("notifications", views.notifications_collection),
    path("notifications/unread-count", views.unread_count),
    path("notifications/<str:notification_id>/read", views.mark_notification_read),
    path("notifications/<str:notification_id>", views.notification_detail),
    path("notifications/mark-all-read", views.mark_all_read),
]
