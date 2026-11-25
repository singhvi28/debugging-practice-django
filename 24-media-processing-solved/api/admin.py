from django.contrib import admin
from .models import MediaJob, MediaAsset


@admin.register(MediaJob)
class MediaJobAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "status", "attempts", "url", "created_at")
    list_filter = ("status",)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "filename", "size_bytes")
