from django.db import models


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
