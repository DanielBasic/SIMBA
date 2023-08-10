from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    thumbnail = models.URLField()
    title = models.CharField(max_length=255)
    original_price = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    free_shipping = models.CharField(max_length=255)
    logistic_type = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    