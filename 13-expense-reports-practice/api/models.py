from django.db import models


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
