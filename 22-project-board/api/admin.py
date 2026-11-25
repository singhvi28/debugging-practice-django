from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "archived")
    list_filter = ("archived",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "title", "done", "version")
    list_filter = ("done",)
