from django.db import models

# Create your models here.

class TaskModel(models.Model):
    email = models.EmailField()
    message = models.TextField()
    status = models.TextField(default='pending')