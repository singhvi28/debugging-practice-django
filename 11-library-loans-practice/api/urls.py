from django.urls import path

from api import views

urlpatterns = [
    path("books", views.list_books),
    path("books/<str:book_id>", views.get_book),
    path("loans/overdue", views.list_overdue_loans),
    path("loans", views.loans_collection),
    path("loans/<str:loan_id>/return", views.return_loan),
]
