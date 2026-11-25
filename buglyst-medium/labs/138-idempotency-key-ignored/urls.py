from django.urls import path

from views import debug_count, post_payment

urlpatterns = [
    path("payments", post_payment),
    path("_debug/count", debug_count),
]
