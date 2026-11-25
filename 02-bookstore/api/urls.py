from django.urls import path

from api import views

urlpatterns = [
    path("books", views.books_collection),
    path("books/<str:book_id>", views.get_book),
    path("book/<str:book_id>", views.delete_book),
    path("cart/<str:cart_id>", views.get_cart),
    path("cart/<str:cart_id>/items", views.add_cart_item),
    path("cart/<str:cart_id>/items/<str:book_id>", views.remove_cart_item),
]
