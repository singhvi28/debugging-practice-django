from django.db import models


class Post(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
