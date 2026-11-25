from django.urls import path

from api import views

urlpatterns = [
    path("reports", views.reports_collection),
    path("reports/<str:report_id>", views.get_report),
    path("reports/<str:report_id>/submit", views.submit_report),
    path("reports/<str:report_id>/approve", views.approve_report),
    path("reports/<str:report_id>/lines", views.add_line_item),
]
