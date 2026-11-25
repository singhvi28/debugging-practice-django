from django.contrib import admin
from .models import Thread, Reply


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")
    search_fields = ("title", "author")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "author", "created_at")
