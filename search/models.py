from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    thumbnail = models.URLField()
    title = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=100)
    free_shipping = models.BooleanField(default=False)
    logistic_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title