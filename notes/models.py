# notes/models.py
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    processed_content = models.TextField(blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True)  # Adjust as needed


    def __str__(self):
        return self.file.name if self.file else self.youtube_url