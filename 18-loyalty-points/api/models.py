from django.db import models


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
