from django.db import models


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
