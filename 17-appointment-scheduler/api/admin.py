from django.contrib import admin
from .models import Provider, Appointment


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialty")
    search_fields = ("name", "specialty")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "client_name", "date", "slot", "status")
    list_filter = ("status",)
