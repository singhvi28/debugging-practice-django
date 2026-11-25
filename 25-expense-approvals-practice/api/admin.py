from django.contrib import admin
from .models import Expense, ApprovalStep


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "status", "approver", "created_at")
    list_filter = ("status",)


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("id", "expense", "approver", "status", "timestamp")
