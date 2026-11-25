from django.urls import path

from api import views

urlpatterns = [
    path("rooms", views.list_rooms),
    path("rooms/<str:room_id>", views.get_room),
    path("bookings", views.bookings_collection),
    path("booking/<str:booking_id>", views.delete_booking),
]
