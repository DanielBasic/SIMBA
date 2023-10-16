from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_stock_quantity_from_ml_ad(url):
    response = requests.get(url, allow_redirects=False)
    if response.status_code > 302:
        raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code} - {response.reason}")
    response = BeautifulSoup(response.content, 'html.parser')
    try:
        stock = response.find(class_='ui-pdp-buybox__quantity__available')
        if not stock:
            stock = 0
        else:
            stock = int(stock.text.split(' ')[0][1:])

        return stock
    except ValueError as e:
        raise(f'Error at get_stock_quantity_from_ml_ad: {e}')

def datetime_stprtime(datetime_inString):
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(datetime_inString, format_string)