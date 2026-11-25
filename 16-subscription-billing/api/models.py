from django.db import models


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
