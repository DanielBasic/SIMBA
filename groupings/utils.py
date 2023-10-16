from product.models import Product, TrackingProduct
from .helpers.image_helpers import get_image
from django.db.models import Q
from django.core.files.base import ContentFile
from datetime import datetime
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
