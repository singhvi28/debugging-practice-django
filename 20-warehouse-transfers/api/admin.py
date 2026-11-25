from django.contrib import admin
from .models import Location, Transfer


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "source", "destination", "quantity", "status")
    list_filter = ("status",)
