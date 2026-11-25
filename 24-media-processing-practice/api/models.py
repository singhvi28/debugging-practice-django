from django.db import models


class MediaJob(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    owner = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default="queued")
    attempts = models.IntegerField(default=0)
    url = models.URLField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} ({self.status})"


class MediaAsset(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    job = models.ForeignKey(MediaJob, on_delete=models.CASCADE, related_name="assets")
    filename = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)

    def __str__(self):
        return self.filename
