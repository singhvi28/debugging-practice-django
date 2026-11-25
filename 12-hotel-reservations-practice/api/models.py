from django.db import models


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
