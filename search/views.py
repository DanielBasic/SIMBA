from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from api_MercadoLivre.getContent import (extract_filters_from_str_dict,
                                         get_access_token,
                                           remove_filters_from_filterList,
                                           tranform_strFilters_list_into_dictFilters_list,
                                           get_availabe_filters,get_all_products)

from .models import Product


def search(request):
  if request.method == "GET":
    app_id = "1481157846018069"
    redirect_url = 'https://simba20-1.jeffersosousa.repl.co'
    client_secret = "1G5RWQSbNZtz1HC1oioNFdIUnOPAs7GU"
    refresh_token = "TG-647222cac299df0001605b9c-1095654007"
    access_token = get_access_token(app_id, client_secret, refresh_token)   
    key_word = request.GET.get("keyWord")

    def getListOfFilters():
      list_of_filters = []
      for key, value in request.GET.items():
          if key.startswith('filter_'):
              filter, value_of_filter, filter_name = value.split(':')
              list_of_filters.append({'filter' : filter, 'value_of_filter': 
                                      value_of_filter, 'filter_name' : filter_name})
      return list_of_filters
    
      
    filters_to_apply = getListOfFilters()

    


    filter_to_exclude = request.GET.get('applied_filter_to_exclude')
    applied_filters = request.GET.get("applied_filters")
    print(applied_filters)
    if applied_filters and applied_filters != '[]':
      applied_filters = extract_filters_from_str_dict(applied_filters)
      print(f'applied filters: {applied_filters}')
      if filter_to_exclude:
        applied_filters = remove_filters_from_filterList(applied_filters, filter_to_exclude)
      applied_filters = tranform_strFilters_list_into_dictFilters_list(applied_filters)
      print(f'filters_to_apply: {filters_to_apply}, applied_filters: {applied_filters}')
      applied_filters = [filters_to_apply.append(filter) for filter in applied_filters]
    
    if access_token:
      available_filters = get_availabe_filters(access_token, key_word, filters_to_apply)
      all_products = get_all_products(access_token, key_word, filters_to_apply)
      print(available_filters, all_products)  

    return render(request, "search/index.html", {"available_filters" : available_filters, "products" : all_products, "keyWord" : key_word, "applied_filters" : filters_to_apply})

  elif request.method == "POST":
    keyWord = request.POST.get("keyWord")
    if not keyWord:
       keyWord = ""

    return redirect(reverse("search")+ "?KeyWord=" + keyWord)
  


def add_product(request):
  if request.method == 'POST':
    product_id = request.POST.get('product_id')
    product_thumbnail = request.POST.get('product_thumbnail')
    product_title = request.POST.get('product_title')
    product_original_price = request.POST.get('product_original_price')
    product_price = request.POST.get('product_price')
    product_condition = request.POST.get('product_condition')
    product_free_shipping = request.POST.get('product_free_shipping')
    product_logistic_type = request.POST.get('product_logistic_type')

    
    produto = Product.objects.create(
      id=product_id,
      thumbnail=product_thumbnail,
      title=product_title,
      original_price=product_original_price,
      price=product_price,
      condition=product_condition,
      free_shipping=product_free_shipping,
      logistic_type=product_logistic_type,
    )

    produto.save()
    messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso')
    return redirect(reverse('search'))
                    
  else:
    return HttpResponse("Método de requisição inválido.")
  

  
