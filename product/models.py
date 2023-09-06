from django.db import models
from django.contrib.auth.models import User
from groupings.models import Group_by_ad
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    image = models.ImageField(upload_to="products_images/", default='products_images/default.png')
    title = models.CharField(max_length=60, null=True)
    price = models.FloatField(null=True)
    user = models.ManyToManyField(User, related_name='products')
    group = models.ManyToManyField(Group_by_ad, related_name='products')
    seller = models.IntegerField(null=True)
    total_sales = models.IntegerField(default=0)
    tracking_since = models.DateTimeField(default=timezone.now)
    is_tracking_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.id
    