import requests
from product.models import Product
def get_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    return response