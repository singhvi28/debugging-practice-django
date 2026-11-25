from django.db import models


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
