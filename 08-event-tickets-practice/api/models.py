from django.db import models


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
