from django.db import models
from django.contrib.auth.models import User
from groupings.models import Group_by_ad
from django.utils import timezone

class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    price = models.FloatField(null=True)
    user = models.ManyToManyField(User, related_name='products')
    group = models.ManyToManyField(Group_by_ad, related_name='products')
    seller = models.IntegerField(null=True)
    tracking_since = models.DateTimeField(default=timezone.now)
    is_tracking_activated = models.BooleanField(default=True)

