from django.contrib import admin
from .models import Book, Cart, CartItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price")
    search_fields = ("title", "author")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "book", "quantity")
