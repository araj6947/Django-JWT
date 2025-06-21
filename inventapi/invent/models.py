from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    barcode = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name