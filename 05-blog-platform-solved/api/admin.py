from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_at")
    search_fields = ("title", "content")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author")
    search_fields = ("author", "text")
