from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from api_MercadoLivre.getContent import (extract_filters_from_str_dict,
                                         get_access_token, searchAdByKeyWord, remove_filters_from_filterList)

from .models import Product


def search(request):
  if request.method == "GET":
    app_id = "1481157846018069"
    redirect_url = 'https://simba20-1.jeffersosousa.repl.co'
    client_secret = "1G5RWQSbNZtz1HC1oioNFdIUnOPAs7GU"
    refresh_token = "TG-647222cac299df0001605b9c-1095654007"
    access_token = get_access_token(app_id, client_secret, refresh_token)   
    key_word = request.GET.get("keyWord")

    def getListOfFilter():
      list_of_filter = {}
      for key, value in request.GET.items():
          if key.startswith('filter_'):
              filter, value_of_filter = value.split(':')
              list_of_filter[filter] = value_of_filter
      return list_of_filter
      
    filters = getListOfFilter()
    filter_to_exclude = request.GET.get('applied_filter_to_exclude')
    applied_filters = request.GET.get("applied_filters")
    if applied_filters:
      applied_filters = extract_filters_from_str_dict(applied_filters)
      if filter_to_exclude:
        applied_filters = remove_filters_from_filterList(applied_filters, filter_to_exclude)
      applied_filters = {applied_filters[i]: applied_filters[i+1] for i in range(0, len(applied_filters), 2)}
      filters.update(applied_filters)
      
    if access_token:
      response = searchAdByKeyWord(access_token, key_word, filters)
      if response.status_code != 200:
        raise Http404("Entrada incorreta")

    return render(request, "search/index.html", {"response" : response.json(), "keyWord" : key_word, "applied_filters" : filters})



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
  
def gerenciar_agrupamento(request):
  if request.method == "GET":
    return redirect(reverse('gerenciar_agrupamento'))