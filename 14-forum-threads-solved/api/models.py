from django.db import models


class Thread(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="replies")
    author = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author} on {self.thread_id}"
