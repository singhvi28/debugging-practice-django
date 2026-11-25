from django.db import models


class Notification(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=128, default="user_default")
    title = models.CharField(max_length=255)
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'READ' if self.read else 'UNREAD'}] {self.title}"
