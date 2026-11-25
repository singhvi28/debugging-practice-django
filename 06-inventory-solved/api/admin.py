from django.contrib import admin
from .models import Product, StockMove


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "stock")
    search_fields = ("sku", "name")


@admin.register(StockMove)
class StockMoveAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "change_type", "quantity", "timestamp")
    list_filter = ("change_type",)
