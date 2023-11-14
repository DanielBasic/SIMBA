from product.models import Product, TrackingProduct
from .helpers.image_helpers import get_image
from django.db.models import Q, Avg
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
import os

class Product_Info:
    def __init__(self, product):
        self.product_id, self.title, self.price, self.seller, self.image_url = product['id'], product['title'], product['price'].replace(',', '.'), product["sellerId"], product["image"]
        self.category_id, self.listing_type_id, self.date_created = product['category_id'], product['listing_type_id'], None
        self.last_updated, self.condition, self.permalink= None, product['condition'], product['permalink']
        self.health, self.status, self.catalog_listing = None, None, product['catalog_listing']
        self.stock_quantity, self.sold_quantity = None, None
        self.free_shipping, self.logistic_type = product['free_shipping'], product['logistic_type']
    def __str__(self):
        return self.product_id

def create_product_object(product):
    try:
        if Product.objects.filter(id=product.product_id).exists():
            print('não foi possível criar o Produto')
            return None
        else:
            product_object = Product(
                id = product.product_id,
                title  = product.title,
                seller_id = product.seller,
                category_id = product.category_id,
                price = product.price,
                listing_type_id = product.listing_type_id,
                date_created = product.date_created,
                last_updated = product.last_updated,
                condition = product.condition,
                permalink = product.permalink,
                logistic_type = product.logistic_type,
                free_shipping =  product.free_shipping,
                health = product.health,
                status = product.status,
                catalog_listing = product.catalog_listing
            )
            product_object.save()
            print(f'foi possível criar o produto: {product_object}')
            return product_object.object_id
    except ValueError as e:
        print(f'error at create_product_object: {e}')

def add_products_into_group(group, user, products):
    try:
        productsAlreadyIntoTheGroup = []
        products_id = {}
        user_products = TrackingProduct.objects.filter(user=user)
        for product in products:
            product_info = Product_Info(product)

            db_product = user_products.filter(Q(product_id=product_info.product_id) & Q(group=group))
            if db_product.exists():
                print(f'product already exists: {product}')
                productsAlreadyIntoTheGroup.append(product_info.product_id)
            else:
                print(f'product doesn"t exists: {product}')
                image = get_image(product_info.image_url)
                filename = os.path.basename(product_info.image_url)
                tracking_product = TrackingProduct(product_id=product_info.product_id,
                                        title=product_info.title,
                                        seller=product_info.seller,
                                        image=f'products_images/{filename}')
                tracking_product.image.save(os.path.basename(product_info.image_url), ContentFile(image.content))
                tracking_product.save()
                tracking_product.user.add(user)
                tracking_product.group.add(group)
                product_id = create_product_object(product_info)
                if product_id:
                    products_id[product_info.product_id] = product_id 

        return productsAlreadyIntoTheGroup, products_id

        
    except ValueError as e:
        print('error at add_products_into_group:' + e)


def getMonthPeriodsDates():
    end_actual_period = datetime.now()
    start_actual_period = end_actual_period - timedelta(days=30)
    end_old_period = start_actual_period - timedelta(days=1)
    start_old_period = end_old_period - timedelta(days=30)

    periods = {'end_actual_period' : end_actual_period, 'start_actual_period' : start_actual_period
               ,'end_old_period' : end_old_period, 'start_old_period' : start_old_period}
    return periods


def getDifferenceBetweenPeriods(old_period_products, actual_period_products):
    if not actual_period_products['avg_price'] or  not old_period_products['avg_price']:
        price_difference_between_periods = 0
    else:
        price_difference_between_periods = round(actual_period_products['avg_price'] - old_period_products['avg_price'], 2)

    if not actual_period_products['avg_health'] or not old_period_products['avg_health']:
        health_difference_between_periods = 0
    else:
        health_difference_between_periods = round(actual_period_products['avg_health'] - old_period_products['avg_health'], 2)

    return {'price_difference_between_periods' : price_difference_between_periods, 'health_difference_between_periods' : health_difference_between_periods}

def getProductsIdsTorGroupByAd(group):
    products_ids = TrackingProduct.objects.filter(group=group).values_list('product_id', flat=True)
    products_ids = list(products_ids)
    return products_ids

def getProductsAvgInfos(products_ids, start_old_period, end_old_period, start_actual_period, end_actual_period):
    old_period_products = Product.objects.filter(id__in=products_ids, date_tracked__range=(start_old_period, end_old_period)).exclude(price__isnull=True, health__isnull=True).aggregate(
    avg_price=Avg('price'),
    avg_health=Avg('health')
    )

    actual_period_products = Product.objects.filter(id__in=products_ids, date_tracked__range=(start_actual_period, end_actual_period)).exclude(price__isnull=True, health__isnull=True).aggregate(
    avg_price=Avg('price'),
    avg_health=Avg('health')
    )

    if not actual_period_products:
        actual_period_products = Product.objects.filter(id__in=products_ids).exclude(price__isnull=True, health__isnull=True).aggregate(
        avg_price = Avg('price'),
        avg_health = Avg('health')
        )
        start_date = Product.objects.filter(id__in=products_ids).earliest('date_tracked')
        end_date = Product.objects.filter(id__in=products_ids).latest('date_tracked')
        date_interval = {'start_date' : start_date, 'end_date' : end_date}
    else:
        date_interval = {'start_date' : start_actual_period, 'end_date' : end_actual_period}
    actual_period_products['avg_price'] = round(actual_period_products['avg_price'], 2) if actual_period_products['avg_price'] else None
    actual_period_products['avg_health'] = round(actual_period_products['avg_health'], 2) if actual_period_products['avg_health'] else None

    return {'date_interval' : date_interval, 'actual_period_products': actual_period_products, 'old_period_products' : old_period_products}

    
def getAvgDataFromGroupByAd(groups, start_old_period, end_old_period, start_actual_period, end_actual_period):
    tracking_infos = {}
    date_interval = {}
    for group in groups:
        avg_info = getProductsAvgInfos(getProductsIdsTorGroupByAd(group), start_old_period, end_old_period, start_actual_period, end_actual_period)
        actual_period_products, old_period_products = avg_info['actual_period_products'], avg_info['old_period_products']
        differenceBetweenPeriods = getDifferenceBetweenPeriods(old_period_products, actual_period_products)
        price_difference_between_periods, health_difference_between_periods = differenceBetweenPeriods['price_difference_between_periods'], differenceBetweenPeriods['health_difference_between_periods']
        date_interval = avg_info['date_interval']
        tracking_infos[group.id] = {'avg_price' : actual_period_products['avg_price'], 'avg_health' : actual_period_products['avg_health'], 'price_variation_percentage' : price_difference_between_periods, 'health_variation_percentage' : health_difference_between_periods}

    return {'tracking_infos' : tracking_infos, 'date_interval' : date_interval}

def getAvgDataFromProducts(products, start_old_period, end_old_period, start_actual_period, end_actual_period):
    tracking_infos = {}
    date_interval = {}
    for product in products:
        avg_info = getProductsAvgInfos([product], start_old_period, end_old_period, start_actual_period, end_actual_period)
        actual_period_products, old_period_products = avg_info['actual_period_products'], avg_info['old_period_products']
        differenceBetweenPeriods = getDifferenceBetweenPeriods(old_period_products, actual_period_products)
        price_difference_between_periods, health_difference_between_periods = differenceBetweenPeriods['price_difference_between_periods'], differenceBetweenPeriods['health_difference_between_periods']
        date_interval = avg_info['date_interval']
        tracking_infos[product.product_id] = {'avg_price' : actual_period_products['avg_price'], 'avg_health' : actual_period_products['avg_health'], 'price_variation_percentage' : price_difference_between_periods, 'health_variation_percentage' : health_difference_between_periods}
        
    return {'tracking_infos' : tracking_infos, 'date_interval' : date_interval}