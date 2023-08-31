from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.


class Group_by_ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="group_by_ad_images/")
    title = models.CharField(max_length=60)
    created_at = models.DateTimeField(default=timezone.now)
    is_tracking_activated = models.BooleanField(default=True)


class Agrupamento_seller(models.Model):
    criador = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)
    logo = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    start_date = models.CharField(max_length=15)
    description = models.CharField(max_length=15)

    def __str__(self):
        return self.title
    
    

