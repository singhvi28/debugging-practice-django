from django.db import models


class Project(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{'x' if self.completed else ' '}] {self.title}"
