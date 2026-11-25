from django.contrib import admin
from .models import ExpenseReport, LineItem


@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "employee", "status", "total_amount")
    list_filter = ("status",)


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "category", "amount")
