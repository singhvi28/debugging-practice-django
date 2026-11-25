from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_monthly")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "plan", "status")
    list_filter = ("status",)
