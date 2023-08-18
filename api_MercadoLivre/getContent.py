import json
import random

import requests
from django.http import Http404

app_id = "1481157846018069"
redirect_url = 'https://simba20-1.jeffersosousa.repl.co'
client_secret = "1G5RWQSbNZtz1HC1oioNFdIUnOPAs7GU"

secure_random = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

authorization_code = "TG-647222b83b397700019b8058-1095654007"
state = "W3TH2Z"

authorization_url = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={app_id}&redirect_uri={redirect_url}&state={secure_random}"



#OBTEM A AUTORIZAÇÃO
def get_authorization(app_id, client_secret, authorization_code, redirect_url):
    payload = f'grant_type=authorization_code&client_id={app_id}&client_secret={client_secret}&code={authorization_code}&redirect_uri={redirect_url}'

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }

    token_url = "https://api.mercadolibre.com/oauth/token"
    response = requests.post(token_url, headers=headers, data=payload)
    return response.json()

token_infos = get_authorization(app_id, client_secret, authorization_code, redirect_url)


# OBTEM O TOKEM DE ACESSO
def get_access_token(app_id, client_secret, refresh_token):
    url = "https://api.mercadolibre.com/oauth/token"

    payload = f'grant_type=refresh_token&client_id={app_id}&client_secret={client_secret}&refresh_token={refresh_token}'
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

refresh_token = "TG-647222cac299df0001605b9c-1095654007"

access_token = get_access_token(app_id, client_secret, refresh_token)



# OBETEM AS INFORMAÇÕES DO ANUNCIO
def getInfoFromAd(access_token, item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    payload = {}
    headers = {
        'Authorization': f'bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response



# ADICONA O FILTRO NAS SOLICITAÇÕES DE PESQUISA DA URL
def addFilterIntoUrlSearchRequest(url, filters):
    try:
        if not filters or filters == []:
            return url
        url_with_filters = url
        for filter in filters:
            type_of_filter = filter['filter']
            value_of_filter = filter['value_of_filter']
            url_with_filters = url_with_filters + "&" + type_of_filter + "=" + value_of_filter
        return url_with_filters
    except TypeError:
        raise

# PESQUISA DO ANUNCIO POR PALAVRA CHAVE
def searchAdByKeyWord(access_token, key_word, filter=None):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={key_word}"

    url = addFilterIntoUrlSearchRequest(url, filter)

    payload = {}
    headers = {
        'Authorization': f'bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


# EXTRAI OS FILTROS
def extract_filters_from_str_dict(text):
    words = []
    start = 0

    while True:
        start_quote = text.find("'", start)
        if start_quote == -1:
            break

        end_quote = text.find("'", start_quote + 1)
        if end_quote == -1:
            break

        word = text[start_quote + 1:end_quote]
        words.append(word)

        start = end_quote + 1

    return words

def find_start_end_indexes(string, substring):
    start_index = None
    end_index = None

    for i in range(len(string)):
        if string[i:i + len(substring)] == substring:
            if start_index is None:
                start_index = i
            end_index = i + len(substring) - 1

    return start_index, end_index

def remove_filter_from_url(url, filter):
    start_index, end_index = find_start_end_indexes(url, filter)

    if start_index is None:
        return url

    new_string = url[:start_index] + url[end_index + 1:]
    return new_string

def remove_filters_from_filterList(filters, filter_type):
    for n, filter in enumerate(filters):
        if filter == filter_type:
            print(f'filter to pop: {filters}')
            print(filter_type)
            for i in range(6):
                print(filters[n - 3])
                filters.pop(n - 3)
    return filters

def tranform_strFilters_list_into_dictFilters_list(values_of_filters):
    filters_list = []
    print(len(values_of_filters))
    for value_filter in range(0, len(values_of_filters), 6):
        filters_list.append({'filter' : values_of_filters[value_filter + 1],
                              'value_of_filter' : values_of_filters[value_filter + 3],
                              'filter_name' : values_of_filters[value_filter + 5]})

    return filters_list


def get_availabe_filters(access_token, key_word, filters_to_apply):
    if access_token:
        response = searchAdByKeyWord(access_token, key_word, filters_to_apply)
        if response.status_code != 200:
            raise Http404("Entrada incorreta")
        else:
            available_filters = response.json()["available_filters"]
            
            return available_filters
            
def get_all_products(access_token, key_word, filters_to_apply):
    response = searchAdByKeyWord(access_token, key_word, filters_to_apply)

    if response.status_code == 200:
        products = response.json()['results']
        return products