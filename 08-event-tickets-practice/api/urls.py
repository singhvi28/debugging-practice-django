from django.urls import path

from api import views

urlpatterns = [
    path("events", views.events_collection),
    path("events/<str:event_id>", views.get_event),
    path("events/<str:event_id>/tickets", views.book_ticket),
    path("tickets/<str:ticket_id>", views.get_ticket),
    path("ticket/<str:ticket_id>", views.delete_ticket),
]
