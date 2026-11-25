from django.db import models


class FileRecord(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    filename = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)
    content_type = models.CharField(max_length=128, default="application/octet-stream")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


class Tag(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    files = models.ManyToManyField(FileRecord, related_name="tags", blank=True)

    def __str__(self):
        return self.name
