from django.db import models


class Book(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=32, blank=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Loan(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrower = models.CharField(max_length=255)
    due_date = models.CharField(max_length=64)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower} borrowed {self.book.title}"
