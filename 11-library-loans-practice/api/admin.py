from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "available_copies")
    search_fields = ("title", "author", "isbn")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "borrower", "due_date", "returned")
    list_filter = ("returned",)
