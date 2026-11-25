from django.contrib import admin
from .models import Event, Ticket


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "capacity")
    search_fields = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "attendee", "price")
    search_fields = ("attendee",)
