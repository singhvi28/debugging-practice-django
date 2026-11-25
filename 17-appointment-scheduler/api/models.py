from django.db import models


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
