#!/usr/bin/env python3
"""Upgrade all 25 Django practice repositories to the canonical Django project structure."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WSGI_TEMPLATE = '''"""
WSGI config for this project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
'''

ASGI_TEMPLATE = '''"""
ASGI config for this project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
'''

SETTINGS_ADDITIONS = '''
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

STATIC_URL = "static/"
'''

DOMAIN_SPECS: dict[str, dict[str, str]] = {
    "01": {
        "models": '''from django.db import models


class Movie(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.year})"


class Review(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.movie_id} - {self.rating} stars"


class Watchlist(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, related_name="watchlists", blank=True)

    def __str__(self):
        return self.name
''',
        "admin": '''from django.contrib import admin
from .models import Movie, Review, Watchlist


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "rating")
    list_filter = ("rating",)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
''',
    },
    "02": {
        "models": '''from django.db import models


class Book(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Cart(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.CharField(max_length=128, default="anonymous")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} ({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.book_id} in {self.cart_id}"
''',
        "admin": '''from django.contrib import admin
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
''',
    },
    "03": {
        "models": '''from django.db import models


class Project(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{'x' if self.completed else ' '}] {self.title}"
''',
        "admin": '''from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "completed")
    list_filter = ("completed",)
    search_fields = ("title",)
''',
    },
    "04": {
        "models": '''from django.db import models


class Recipe(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.quantity} {self.name} for {self.recipe.name}"
''',
        "admin": '''from django.contrib import admin
from .models import Recipe, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "recipe")
    search_fields = ("name",)
''',
    },
    "05": {
        "models": '''from django.db import models


class Post(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
''',
        "admin": '''from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_at")
    search_fields = ("title", "content")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author")
    search_fields = ("author", "text")
''',
    },
    "06": {
        "models": '''from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class StockMove(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="moves")
    change_type = models.CharField(max_length=32)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change_type} {self.quantity} ({self.product.sku})"
''',
        "admin": '''from django.contrib import admin
from .models import Product, StockMove


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "stock")
    search_fields = ("sku", "name")


@admin.register(StockMove)
class StockMoveAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "change_type", "quantity", "timestamp")
    list_filter = ("change_type",)
''',
    },
    "07": {
        "models": '''from django.db import models


class Track(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in seconds")

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Playlist(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track, related_name="playlists", blank=True)

    def __str__(self):
        return self.name
''',
        "admin": '''from django.contrib import admin
from .models import Track, Playlist


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "duration")
    search_fields = ("title", "artist")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
''',
    },
    "08": {
        "models": '''from django.db import models


class Event(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=64)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    attendee = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.attendee} - {self.event.name}"
''',
        "admin": '''from django.contrib import admin
from .models import Event, Ticket


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "capacity")
    search_fields = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "attendee", "price")
    search_fields = ("attendee",)
''',
    },
    "09": {
        "models": '''from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    max_students = models.IntegerField(default=30)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student_email = models.EmailField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_email} in {self.course.title}"
''',
        "admin": '''from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "instructor", "max_students")
    search_fields = ("title", "instructor")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "student_email", "enrolled_at")
    search_fields = ("student_email",)
''',
    },
    "10": {
        "models": '''from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    customer_email = models.EmailField()
    status = models.CharField(max_length=32, default="pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.order_id}"
''',
        "admin": '''from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_email", "status", "total", "created_at")
    list_filter = ("status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
''',
    },
    "11": {
        "models": '''from django.db import models


class Book(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=32, blank=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Loan(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrower = models.CharField(max_length=255)
    due_date = models.CharField(max_length=64)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower} borrowed {self.book.title}"
''',
        "admin": '''from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "available_copies")
    search_fields = ("title", "author", "isbn")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "borrower", "due_date", "returned")
    list_filter = ("returned",)
''',
    },
    "12": {
        "models": '''from django.db import models


class Room(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    room_number = models.CharField(max_length=32)
    room_type = models.CharField(max_length=64)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"


class Reservation(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    guest_name = models.CharField(max_length=255)
    check_in = models.CharField(max_length=64)
    check_out = models.CharField(max_length=64)

    def __str__(self):
        return f"Reservation {self.id} for {self.guest_name}"
''',
        "admin": '''from django.contrib import admin
from .models import Room, Reservation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "room_type", "price_per_night")
    list_filter = ("room_type",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest_name", "check_in", "check_out")
    search_fields = ("guest_name",)
''',
    },
    "13": {
        "models": '''from django.db import models


class ExpenseReport(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    employee = models.CharField(max_length=255)
    status = models.CharField(max_length=32, default="draft")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.title} ({self.employee})"


class LineItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    report = models.ForeignKey(ExpenseReport, on_delete=models.CASCADE, related_name="line_items")
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} (${self.amount})"
''',
        "admin": '''from django.contrib import admin
from .models import ExpenseReport, LineItem


@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "employee", "status", "total_amount")
    list_filter = ("status",)


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "category", "amount")
''',
    },
    "14": {
        "models": '''from django.db import models


class Thread(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="replies")
    author = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author} on {self.thread_id}"
''',
        "admin": '''from django.contrib import admin
from .models import Thread, Reply


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")
    search_fields = ("title", "author")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "author", "created_at")
''',
    },
    "15": {
        "models": '''from django.db import models


class FileRecord(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    filename = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)
    content_type = models.CharField(max_length=128, default="application/octet-stream")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


class Tag(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    files = models.ManyToManyField(FileRecord, related_name="tags", blank=True)

    def __str__(self):
        return self.name
''',
        "admin": '''from django.contrib import admin
from .models import FileRecord, Tag


@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "filename", "size_bytes", "content_type", "uploaded_at")
    search_fields = ("filename",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
''',
    },
    "16": {
        "models": '''from django.db import models


class Plan(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.price_monthly}/mo)"


class Subscription(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=128)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")
    status = models.CharField(max_length=32, default="active")
    renews_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription {self.id} ({self.user_id})"
''',
        "admin": '''from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_monthly")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "plan", "status")
    list_filter = ("status",)
''',
    },
    "17": {
        "models": '''from django.db import models


class Provider(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=128)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"


class Appointment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="appointments")
    client_name = models.CharField(max_length=255)
    date = models.CharField(max_length=32)
    slot = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default="confirmed")

    def __str__(self):
        return f"{self.client_name} with {self.provider.name} at {self.slot}"
''',
        "admin": '''from django.contrib import admin
from .models import Provider, Appointment


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialty")
    search_fields = ("name", "specialty")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "client_name", "date", "slot", "status")
    list_filter = ("status",)
''',
    },
    "18": {
        "models": '''from django.db import models


class Account(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    owner = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner} ({self.balance} pts)"


class LedgerEntry(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="entries")
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount:+d} pts for {self.account_id}"
''',
        "admin": '''from django.contrib import admin
from .models import Account, LedgerEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "balance")


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "amount", "reason", "created_at")
''',
    },
    "19": {
        "models": '''from django.db import models


class Notification(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=128, default="user_default")
    title = models.CharField(max_length=255)
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'READ' if self.read else 'UNREAD'}] {self.title}"
''',
        "admin": '''from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "read", "created_at")
    list_filter = ("read",)
    search_fields = ("title", "body")
''',
    },
    "20": {
        "models": '''from django.db import models


class Location(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    sku = models.CharField(max_length=64)
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="outgoing_transfers")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="incoming_transfers")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=32, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer {self.sku} ({self.quantity}) from {self.source} to {self.destination}"
''',
        "admin": '''from django.contrib import admin
from .models import Location, Transfer


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "source", "destination", "quantity", "status")
    list_filter = ("status",)
''',
    },
    "21": {
        "models": '''from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Cart(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Order(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.CharField(max_length=128)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32, default="paid")
    idempotency_key = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} ({self.user}) - {self.status}"
''',
        "admin": '''from django.contrib import admin
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
''',
    },
    "22": {
        "models": '''from django.db import models


class Project(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=128)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"[{'x' if self.done else ' '}] {self.title} (v{self.version})"
''',
        "admin": '''from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "archived")
    list_filter = ("archived",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "title", "done", "version")
    list_filter = ("done",)
''',
    },
    "23": {
        "models": '''from django.db import models


class Shipment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    owner = models.CharField(max_length=128)
    status = models.CharField(max_length=64, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment {self.id} ({self.status})"


class Checkpoint(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="checkpoints")
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shipment_id}: {self.status} at {self.location}"
''',
        "admin": '''from django.contrib import admin
from .models import Shipment, Checkpoint


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "status", "created_at")
    list_filter = ("status",)


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = ("id", "shipment", "location", "status", "timestamp")
''',
    },
    "24": {
        "models": '''from django.db import models


class MediaJob(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    owner = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default="queued")
    attempts = models.IntegerField(default=0)
    url = models.URLField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} ({self.status})"


class MediaAsset(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    job = models.ForeignKey(MediaJob, on_delete=models.CASCADE, related_name="assets")
    filename = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)

    def __str__(self):
        return self.filename
''',
        "admin": '''from django.contrib import admin
from .models import MediaJob, MediaAsset


@admin.register(MediaJob)
class MediaJobAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "status", "attempts", "url", "created_at")
    list_filter = ("status",)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "filename", "size_bytes")
''',
    },
    "25": {
        "models": '''from django.db import models


class Expense(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32, default="pending")
    approver = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense {self.id} (${self.amount}) - {self.status}"


class ApprovalStep(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="approval_steps")
    approver = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.approver}: {self.status} on {self.expense_id}"
''',
        "admin": '''from django.contrib import admin
from .models import Expense, ApprovalStep


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "status", "approver", "created_at")
    list_filter = ("status",)


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("id", "expense", "approver", "status", "timestamp")
''',
    },
}


APPS_PY_TEMPLATE = '''from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
'''

DATABASES_TEMPLATE = '''
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
'''

def upgrade_repo(repo_dir: Path) -> tuple[bool, str]:
    num = repo_dir.name[:2]
    if num not in DOMAIN_SPECS:
        return False, f"Unknown domain number {num}"

    # Unlock directory write permissions if read-only
    subprocess.run(["chmod", "-R", "u+w", str(repo_dir)], check=True)

    # 1. config/wsgi.py
    wsgi_file = repo_dir / "config/wsgi.py"
    if not wsgi_file.exists():
        wsgi_file.write_text(WSGI_TEMPLATE)

    # 2. config/asgi.py
    asgi_file = repo_dir / "config/asgi.py"
    if not asgi_file.exists():
        asgi_file.write_text(ASGI_TEMPLATE)

    # 3. api/__init__.py and api/apps.py
    api_dir = repo_dir / "api"
    api_init = api_dir / "__init__.py"
    if not api_init.exists():
        api_init.write_text("")

    api_apps = api_dir / "apps.py"
    if not api_apps.exists():
        api_apps.write_text(APPS_PY_TEMPLATE)

    # 4. tests/__init__.py and pytest.ini
    tests_dir = repo_dir / "tests"
    if tests_dir.exists():
        tests_init = tests_dir / "__init__.py"
        if not tests_init.exists():
            tests_init.write_text("")

    pytest_ini = repo_dir / "pytest.ini"
    if pytest_ini.exists():
        ini_text = pytest_ini.read_text()
        if "pythonpath" not in ini_text:
            pytest_ini.write_text(ini_text.strip() + "\npythonpath = .\n")

    # 5. config/settings.py
    settings_file = repo_dir / "config/settings.py"
    if settings_file.exists():
        settings_text = settings_file.read_text()
        
        # Ensure INSTALLED_APPS includes 'api'
        if re.search(r'INSTALLED_APPS\s*=\s*\[\s*\]', settings_text):
            settings_text = re.sub(
                r'INSTALLED_APPS\s*=\s*\[\s*\]',
                'INSTALLED_APPS = ["django.contrib.contenttypes", "api"]',
                settings_text
            )
        elif "INSTALLED_APPS" in settings_text and '"api"' not in settings_text:
            settings_text = re.sub(
                r'INSTALLED_APPS\s*=\s*\[',
                'INSTALLED_APPS = [\n    "api",',
                settings_text
            )

        # Ensure DATABASES is configured
        if "DATABASES" not in settings_text:
            settings_text += "\n" + DATABASES_TEMPLATE

        # Ensure DEFAULT_AUTO_FIELD
        if "DEFAULT_AUTO_FIELD" not in settings_text:
            settings_text += '\nDEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"\n'

        # Ensure WSGI_APPLICATION, ASGI_APPLICATION, TEMPLATES, STATIC_URL
        if "WSGI_APPLICATION" not in settings_text:
            settings_text = settings_text.rstrip() + "\n" + SETTINGS_ADDITIONS

        settings_file.write_text(settings_text)

    # 6. api/migrations/__init__.py
    migrations_dir = repo_dir / "api/migrations"
    migrations_dir.mkdir(exist_ok=True)
    mig_init = migrations_dir / "__init__.py"
    if not mig_init.exists():
        mig_init.write_text("")

    # 7. api/models.py
    models_file = repo_dir / "api/models.py"
    models_file.write_text(DOMAIN_SPECS[num]["models"])

    # 8. api/admin.py
    admin_file = repo_dir / "api/admin.py"
    admin_file.write_text(DOMAIN_SPECS[num]["admin"])

    # 9. Generate migration if needed
    try:
        subprocess.run(
            [sys.executable, "manage.py", "makemigrations", "api"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return False, f"makemigrations failed in {repo_dir.name}: {e.stderr}"

    # 10. Check django system integrity
    try:
        subprocess.run(
            [sys.executable, "manage.py", "check"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return False, f"manage.py check failed in {repo_dir.name}: {e.stderr}"

    return True, "Upgraded successfully"


def main():
    repo_dirs = sorted(
        [
            p
            for p in ROOT.glob("[0-9][0-9]*")
            if p.is_dir() and (p / "manage.py").exists() and (p / "api").exists()
        ]
    )
    print(f"Discovered {len(repo_dirs)} target repositories to upgrade.")

    failed = []
    success_count = 0
    for r in repo_dirs:
        ok, msg = upgrade_repo(r)
        if ok:
            success_count += 1
            print(f" [OK] {r.name}")
        else:
            failed.append((r.name, msg))
            print(f" [FAIL] {r.name}: {msg}")

    print("\n" + "=" * 50)
    print(f"Summary: {success_count}/{len(repo_dirs)} repos successfully upgraded.")
    if failed:
        print(f"{len(failed)} repos failed:")
        for name, err in failed:
            print(f"  - {name}: {err}")
        sys.exit(1)
    else:
        print("All repos upgraded to canonical Django directory structure!")


if __name__ == "__main__":
    main()
