from celery import shared_task
from .models import Product

@shared_task(name='addLastUpdadeProductInDb')
def addLastUpdadeProductInDb():
    Product.objects.values(id).distinct()