from django.contrib import admin
from .models import Room, Reservation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "room_type", "price_per_night")
    list_filter = ("room_type",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest_name", "check_in", "check_out")
    search_fields = ("guest_name",)
