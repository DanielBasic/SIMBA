from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    data_de_nascimento = models.DateField()