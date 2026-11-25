from django.urls import path

from api import views

urlpatterns = [
    path("providers", views.list_providers),
    path("providers/<str:provider_id>", views.get_provider),
    path("appointments", views.appointments_collection),
    path("appointments/<str:appointment_id>", views.appointment_detail),
    path("appointments/<str:appointment_id>/cancel", views.cancel_appointment),
]
