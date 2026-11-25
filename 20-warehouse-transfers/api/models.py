from django.db import models


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
