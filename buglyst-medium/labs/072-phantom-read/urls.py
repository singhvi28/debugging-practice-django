from django.urls import path

from views import admin_reset, txn_begin, txn_commit, txn_read, txn_rollback, txn_write

urlpatterns = [
    path("txn/<str:txn_id>/begin", txn_begin),
    path("txn/<str:txn_id>/write", txn_write),
    path("txn/<str:txn_id>/read/<str:key>", txn_read),
    path("txn/<str:txn_id>/commit", txn_commit),
    path("txn/<str:txn_id>/rollback", txn_rollback),
    path("admin/reset", admin_reset),
]
