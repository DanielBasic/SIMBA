from celery import shared_task
from .models import Product
from api_MercadoLivre.getContent import getPeriodicInfoProduct, get_ad_info_with_att, get_access_token
from .utils import get_stock_quantity_from_ml_ad
from datetime import timedelta
from django.db.models import Q
from .utils import datetime_stprtime
from decouple import config


@shared_task(name='addLastUpdadeProductInDb')
def addLastUpdadeProductInDb():
    products_ids = Product.objects.values(id).distinct().all()
    products_infos = getPeriodicInfoProduct(products_ids, ['id'])

@shared_task(name='add_stock_info_in_db')
def add_stock_info_in_db(url, initial_quantity, objt_product_id):
    try:
        stock_quantity = get_stock_quantity_from_ml_ad(url)
        if stock_quantity: 
            sold_quantity = int(initial_quantity) - stock_quantity
        else:
            sold_quantity = None

        product = Product.objects.get(object_id=objt_product_id)
        one_day_before = product.tracking_since - timedelta(days=1)
        last_stock_quantity = Product.objects.filter(tracking_since__date=one_day_before, id=product.id)
        if not last_stock_quantity.exists():
            daily_sales = 0
        else:
            daily_sales = sold_quantity - last_stock_quantity.first().sold_quantity
        
        product.sold_quantity = sold_quantity
        product.stock_quantity = stock_quantity
        product.daily_sales = daily_sales
        product.save()

    except ValueError as e:
        raise f'Error at add_stock_infos_in_db: {e}'

@shared_task(name='add_geral_infos_product_in_db')
def add_geral_infos_product_in_db(products):
    if bool(products):
        attributes = ['id', 'date_created', 'last_updated', 'health', 'initial_quantity', 'status', 'permalink']
        products_id = list(products.keys())
        app_id = config('APP_ID')
        client_secret = config('CLIENT_SECRET')
        refresh_token = config('REFRESH_TOKEN')
        access_token = get_access_token(app_id, client_secret, refresh_token)
        ads_data = get_ad_info_with_att(access_token, products_id, attributes)
        if access_token:
            for ad in ads_data:
                if ad['code'] == 200:
                    body = ad['body']
                    object_product_id = products[body['id']]
                    add_stock_info_in_db.delay(body['permalink'], body['initial_quantity'], object_product_id)
                    try:
                        product = Product.objects.get(object_id = object_product_id)
                        product.date_created = datetime_stprtime(body['date_created'])
                        product.last_updated = datetime_stprtime(body['last_updated'])
                        product.health = body['health']
                        product.status = body['status']
                        product.save()

                    except Product.DoesNotExist:
                        raise ('Product DoesNotExist, tried at "add_geral_infos_product_in_db"')