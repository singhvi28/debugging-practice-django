from django.urls import path

from views import debug_processed, receive_webhook

urlpatterns = [
    path("webhooks", receive_webhook),
    path("_debug/processed", debug_processed),
]
