from django.urls import path

from views import (
    admin_half_open,
    debug_downstream_calls,
    get_circuit,
    proxy_request,
    proxy_success,
)

urlpatterns = [
    path("proxy", proxy_request),
    path("proxy/success", proxy_success),
    path("admin/half-open", admin_half_open),
    path("circuit", get_circuit),
    path("_debug/downstream-calls", debug_downstream_calls),
]
