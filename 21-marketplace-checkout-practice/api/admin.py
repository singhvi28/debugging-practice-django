from django.contrib import admin
from .models import Product, Cart, CartLine, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")


@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created_at")
    list_filter = ("status",)
