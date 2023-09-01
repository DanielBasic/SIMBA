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
                                           get_availabe_filters,get_all_products,
                                           searchAdByKeyWord,
                                           get_filter_to_offset, str_to_dict)
from groupings.forms import GroupByAd_form
from groupings.models import Group_by_ad


from api_MercadoLivre.getContent import (
    extract_filters_from_str_dict, get_access_token, get_all_products,
    get_availabe_filters, get_filter_to_offset, remove_filters_from_filterList,
    searchAdByKeyWord, tranform_strFilters_list_into_dictFilters_list)
from groupings.forms import GroupByAd_form
from groupings.models import Group_by_ad
from utils_objects import Pagination

from .models import Product


@login_required
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

    if applied_filters and applied_filters != '[]':
      applied_filters = extract_filters_from_str_dict(applied_filters)
      if filter_to_exclude:
        applied_filters = remove_filters_from_filterList(applied_filters, filter_to_exclude)
      applied_filters = tranform_strFilters_list_into_dictFilters_list(applied_filters)
      for filter in applied_filters:
        filters_to_apply.append(filter)
    
    number_of_pages = 1
    if access_token:
      response = searchAdByKeyWord(access_token, key_word, filters_to_apply)
      if response:
        response = response.json()
        quantity_of_results = response['paging']['primary_results']
        number_of_pages = quantity_of_results // 50 + (1 if quantity_of_results % 50 != 0 else 0)
    action_page = request.GET.get('action_page')
    current_page = 1
    pagination_action = None
    if action_page:
        pagination_action = action_page
    page = request.GET.get('current_page')
    if page:
      if page.isnumeric():
        current_page = int(page)
    pagination = Pagination(number_of_pages=number_of_pages, current_page=current_page)
    if pagination_action:
      if pagination_action == 'set_next_page':
        pagination.set_next_page()

      elif pagination_action == 'set_previous_page':
        pagination.set_previous_page()
    offset = get_filter_to_offset(pagination.current_page, pagination.number_of_pages)

    if offset:
      filters_to_apply.append(offset)
    if access_token:
      available_filters = get_availabe_filters(access_token, key_word, filters_to_apply)
      all_products = get_all_products(access_token, key_word, filters_to_apply)
    if offset:
      filters_to_apply.pop()

    current_user = request.user
    groupByAd_form = GroupByAd_form()
    all_GroupByAd = Group_by_ad.objects.filter(user=current_user)
    if len(all_GroupByAd) == 0:
      all_GroupByAd = None

    return render(request, "search/index.html", {"pagination" : pagination,"available_filters" : available_filters, "products" : all_products, "keyWord" : key_word, "applied_filters" : filters_to_apply, 'all_GroupByAd' : all_GroupByAd, 'groupByAd_form' : groupByAd_form})

  elif request.method == "POST":
    keyWord = request.POST.get("keyWord")
    if not keyWord:
       keyWord = ""
    

    return redirect(reverse("search")+ "?KeyWord=" + keyWord)


@login_required
def add_products_group_by(request):
  if request.method == "POST":
    form_image_title = GroupByAd_form(request.POST, request.FILES)
    products = request.POST.getlist('products_info')
    products = [str_to_dict(product) for product in products]
    if form_image_title.is_valid:
      pass
   
@login_required
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
  

  