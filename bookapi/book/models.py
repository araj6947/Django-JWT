from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

