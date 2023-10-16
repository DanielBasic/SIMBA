from django.db import models
from django.contrib.auth.models import User
from groupings.models import Group_by_ad
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TrackingProduct(models.Model):
    object_id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=30)
    image = models.ImageField(upload_to="products_images/", default='products_images/default.png')
    title = models.CharField(max_length=60, null=True)
    user = models.ManyToManyField(User, related_name='products')
    group = models.ManyToManyField(Group_by_ad, related_name='products')
    seller = models.IntegerField(null=True)
    tracking_since = models.DateTimeField(default=timezone.now)
    is_tracking_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.product_id
    
class Product(models.Model):
    object_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    title  = models.CharField(max_length=90)
    seller_id = models.IntegerField()
    category_id = models.CharField(max_length=30)
    price = models.FloatField()
    stock_quantity = models.IntegerField(null=True)
    sold_quantity = models.IntegerField(null=True)
    daily_sales = models.IntegerField(null=True, default=0)
    listing_type_id = models.CharField(max_length=30)
    date_created = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)
    condition = models.CharField(max_length=30)
    permalink = models.CharField(max_length=300)
    logistic_type = models.CharField(max_length=30, null=True)
    free_shipping = models.BooleanField(null=True)
    health = models.FloatField(null=True)
    status = models.CharField(max_length=30, null=True)
    catalog_listing = models.BooleanField()
    tracking_since = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id