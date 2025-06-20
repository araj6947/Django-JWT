from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    barcode = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.category})"