from django.contrib import admin
from .models import FileRecord, Tag


@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "filename", "size_bytes", "content_type", "uploaded_at")
    search_fields = ("filename",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
