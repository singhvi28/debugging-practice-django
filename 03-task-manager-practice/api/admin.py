from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "completed")
    list_filter = ("completed",)
    search_fields = ("title",)
