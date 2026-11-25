from django.urls import path

from views import latency_metrics

urlpatterns = [
    path("metrics/latency", latency_metrics),
]
