from django.contrib import admin
from .models import Shipment, Checkpoint


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "status", "created_at")
    list_filter = ("status",)


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = ("id", "shipment", "location", "status", "timestamp")
