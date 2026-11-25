from django.urls import path

from views import get_webhooks, post_event, post_reconnect

urlpatterns = [
    path("reconnect", post_reconnect),
    path("event", post_event),
    path("webhooks", get_webhooks),
]
