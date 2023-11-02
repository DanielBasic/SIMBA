from bs4 import BeautifulSoup
import requests
from datetime import datetime

def is_ad_paused(url):
    response = requests.get(url, allow_redirects=False)
    if response.status_code > 302:
        raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code} - {response.reason}")
    response = BeautifulSoup(response.content, 'html.parser')

    paused = response.find(class_='ui-pdp-container_row ui-pdp-container_row--item-status-short-description-message')
    if paused:
        return True
    else:
        return False

def get_stock_quantity_from_ml_ad(url):
    
    if is_ad_paused(url):
        return 0

    response = requests.get(url)
    if response.status_code > 302:
        raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code} - {response.reason}")
    response = BeautifulSoup(response.content, 'html.parser')
    try:
        stock = response.find(class_='ui-pdp-buybox_quantity_available')
        if not stock:
            stock = response.find(class_='ui-pdp-action-row__subtitle')
            if not stock:
                stock = None
            else:
                stock = int(stock.text.split(' ')[0][1:])

        else:
            stock = int(stock.text.split(' ')[0][1:])

        return stock
    except ValueError as e:
        raise(f'Error at get_stock_quantity_from_ml_ad: {e}')
    


def datetime_stprtime(datetime_inString):
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(datetime_inString, format_string)