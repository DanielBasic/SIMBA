from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Agrupamento(models.Model):
    criador = models.ForeignKey(User,  on_delete=models.CASCADE )
    logo = models.CharField(max_length=15)
    title = models.CharField(max_length=15)
    start_date = models.CharField(max_length=15)
    description = models.CharField(max_length=15)

    def __str__(self):
        return self.title
    


class Agrupamento_seller(models.Model):
    criador = models.ForeignKey(User,  on_delete=models.CASCADE )
    logo = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    start_date = models.CharField(max_length=15)
    description = models.CharField(max_length=15)

    def __str__(self):
        return self.title
    
    

