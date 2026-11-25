from django.urls import path

from views import debug_query_count, debug_work_units, orders

urlpatterns = [
    path("orders", orders),
    path("_debug/work-units", debug_work_units),
    path("_debug/query-count", debug_query_count),
]
