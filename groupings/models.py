from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.utils import timezone

# Create your models here.


class Group_by_ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="group_by_ad_images/", default="group_by_ad_images/default.png", null=True)
    title = models.CharField(max_length=60)
    created_at = models.DateTimeField(default=timezone.now)
    is_tracking_activated = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


# class Group_by_seller(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)
#     logo = models.CharField(max_length=15)
#     store_name = models.CharField(max_length=15)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_tracking_activated = models.BooleanField(default=True)


    
    

