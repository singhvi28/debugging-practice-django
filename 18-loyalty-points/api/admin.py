from django.contrib import admin
from .models import Account, LedgerEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "balance")


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "amount", "reason", "created_at")
