from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import GroupByAd_form
from api_MercadoLivre.getContent import str_to_dict, get_visits_from_product
from django.db.models import Q, Avg
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from product.models import Product, TrackingProduct
from .models import Group_by_ad
from product.tasks import add_geral_infos_product_in_db
from .utils import add_products_into_group
from django.core.serializers import serialize

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from product.models import Product, TrackingProduct
from django.db.models import Q
from api_MercadoLivre.getContent import getInfoFromProduct, get_access_token
from decouple import config
from django.contrib.auth.decorators import login_required

from .utils import add_products_into_group, getMonthPeriodsDates, getAvgDataFromGroupByAd, getAvgDataFromProducts, priceVariationsOfGroupByAd
import os
from django.core.exceptions import ObjectDoesNotExist

@login_required
def create_new_groupByAd(request):
    if request.method == "GET":
        return render(request, "groupings/create_new_groupByAd.html")
    
    elif request.method == "POST":
        data_groupByAd = GroupByAd_form(request.POST, request.FILES)
        if data_groupByAd.is_valid():
            cleaned_data = data_groupByAd.cleaned_data
            image = cleaned_data['image']
            title = cleaned_data['title']
            
           
            try:
                existing_groupByAd = Group_by_ad.objects.get(title=title)
                messages.add_message(request, constants.ERROR, 'Já existe um agrupamento com esse título.')
                return redirect(reverse('groupByAd_management'))
            except ObjectDoesNotExist:
              
                groupByAd = Group_by_ad(image=image, title=title, user=request.user)
                groupByAd.save()
                messages.add_message(request, constants.SUCCESS, 'Agrupamento criado com sucesso')
                return redirect(reverse('groupByAd_management'))
        
        messages.add_message(request, constants.ERROR, 'Adicione uma imagem e um título válido')
        return redirect(reverse('groupByAd_management'))
  



    
@login_required
def groupByAd_management(request):
  if request.method == "GET":
    groupByAd_all = Group_by_ad.objects.filter(user=request.user)
    form_groupByAd = GroupByAd_form()
    groups = Group_by_ad.objects.filter(user=request.user)
  
    periods = getMonthPeriodsDates()
    start_old_period, end_old_period = periods['start_old_period'], periods['end_old_period']
    start_actual_period, end_actual_period = periods['start_actual_period'], periods['end_actual_period']

    avg_infos = getAvgDataFromGroupByAd(groups, start_old_period, end_old_period, start_actual_period, end_actual_period)

    tracking_infos, date_interval = avg_infos['tracking_infos'], avg_infos['date_interval']
    print(priceVariationsOfGroupByAd(groups))
    return render(request, "groupings/groupByAd_management.html", {'groupByAd_all': groupByAd_all , 'groupByAd_form' : form_groupByAd, 'tracking_infos' : tracking_infos, 'date_interval' : date_interval})


@login_required
def add_products_into_GroupByAd(request):
  if request.method == "GET":
    return redirect(reverse("groupByAd_management"))
  if request.method == "POST":
    try:
      groupByAd_id = request.POST.get("groupByAd_id")
      products = request.POST.getlist("products_info")
      products = [str_to_dict(product) for product in products]
      group = Group_by_ad.objects.filter(id=int(groupByAd_id)).first()
      current_user = request.user
      if group and products:
        product_already_in_group, products_id = add_products_into_group(group, current_user, products)
        add_geral_infos_product_in_db.delay(products_id)
        if product_already_in_group:
          messages.add_message(request, messages.ERROR , f'Não foi possível adicionar os seguinte produtos, pois eles já estão adicionados nesse agrupamento: {product_already_in_group}')
        else:
          messages.add_message(request, messages.SUCCESS,'Monitoramento iniciado com sucesso')
      return redirect(f"/groupings/group/?group_id={group.id}")
    except ValueError as e:
      return redirect(reverse('search'))
    


@login_required
def create_new_GroupByAd_addProductsInIt(request):
  if request.method == "GET":
    return redirect(reverse("search"))
  elif request.method == "POST":
    try:
      
      form_image_title = GroupByAd_form(request.POST, request.FILES)
      products = request.POST.getlist('products_info')
      products = [str_to_dict(product) for product in products]
      current_user = request.user
      users_group = Group_by_ad.objects.filter(user=request.user)
      group = None
      
      if form_image_title.is_valid():
        title, image = form_image_title.cleaned_data['title'], form_image_title.cleaned_data['image']
        group_exist = users_group.filter(title=title).first()
        if group_exist:
          messages.add_message(request, constants.ERROR,'Ja existe um agrupamento com esse nome')
        else:
          group = Group_by_ad(title=title, image=image, user=current_user)
          group.save()

      if group and products:
        product_already_in_group, products_id = add_products_into_group(group, current_user, products)
        print(f'products ids: {products_id}')
        add_geral_infos_product_in_db.delay(products_id)

        if product_already_in_group:
          messages.add_message(request, messages.INFO , f'Não foi possível adicionar os seguinte produtos, pois eles já estão adicionados nesse agrupamento: {product_already_in_group}')
        else:
          messages.add_message(request, messages.SUCCESS, f'Monitoramento iniciado com sucesso')
        return redirect(f"/groupings/group/?group_id={group.id}")
      
      return redirect(reverse('search'))

    except ValueError as e:
      print(f"Error at 'create_new_GroupByAd_addProductsInIt' create: {e}")
      return redirect(reverse("search"))
    
 
    
@login_required
def groupByAd_details(request):
  if request.method == "GET":
    group_id = request.GET.get("group_id")
    if group_id.isnumeric():
      group_id = int(group_id)
      group = Group_by_ad.objects.filter(id=group_id).first()
      user = request.user
      products = TrackingProduct.objects.filter(Q(user=user) & Q(group=group))
      
      periods = getMonthPeriodsDates()
      start_old_period, end_old_period = periods['start_old_period'], periods['end_old_period']
      start_actual_period, end_actual_period = periods['start_actual_period'], periods['end_actual_period']

      avg_infos = getAvgDataFromProducts(products, start_old_period, end_old_period, start_actual_period, end_actual_period)

      tracking_infos, date_interval = avg_infos['tracking_infos'], avg_infos['date_interval']
      print(priceVariationsOfGroupByAd)
    else:
      raise TypeError("The group_id must be a int type")
    return render(request, "groupings/groupByAd_details.html", {'products' : products, 'group_id' : group_id, 'tracking_infos' : tracking_infos, 'date_interval' : date_interval})


# PARAR O AGRUPAMENTO
@login_required
def toggle_tracking_groupByAd(request, group_id):
    if request.method == "GET":
      group = get_object_or_404(Group_by_ad, id=group_id)
      group.is_tracking_activated
      return render(request, 'groupByAd_management.html', group.is_tracking_activated)
    
    if request.method == "POST":
        group = get_object_or_404(Group_by_ad, id=group_id)
        status = not group.is_tracking_activated
        tracking_products = TrackingProduct.objects.filter(group=group)
        if tracking_products.exists():
          for product in tracking_products:
            product.is_tracking_activated = status
            product.save()
        group.is_tracking_activated = status
        group.save()
        
        messages.add_message(request, constants.SUCCESS, 'O Monitoramento desse agrupamento foi alterado')
        return redirect(reverse('groupByAd_management'))
    else:
        messages.add_message(request, constants.SUCCESS, 'Não foi possível alterar o monitoramento desse agrupamento')


# EDITAR O AGRUPAMENTO
@login_required
def edit_groupByAd(request):
    if request.method == "POST":
      image = request.FILES.get("image_to_modify")
      title = request.POST.get("title_to_modify")
      group_id = request.POST.get("group_id_modify")
      ad_group = Group_by_ad.objects.get(id=group_id)
      users_group = Group_by_ad.objects.filter(user=request.user, title=title)

      if not users_group.exists():
        if title:
          ad_group.title = title
      if image:
        ad_group.image = image
      
      ad_group.save() 

      if users_group.exists():
        if ad_group.title == title:
          pass
        else:
          messages.add_message(request, constants.ERROR,'Ja existe um agrupamento com esse nome')   
      return redirect(reverse('groupByAd_management'))
    elif request.method == "GET":
      return redirect(reverse('groupByAd_management'))

    return render(request, "groupings/groupByAd_details.html", {'products' : products, 'tracking_infos' : tracking_infos, 'date_interval' : date_interval})

         
# EXCLUIR UM AGRUPAMENTO
@login_required
def exclude_groupByAd(request, group_id):
  if request.method == "POST":
    group = Group_by_ad.objects.filter(id=group_id).first()
    if group:
      tracking_products = TrackingProduct.objects.filter(group=group)
      for product in tracking_products:
        product.delete()
      group.delete()
     
      return redirect(reverse('groupByAd_management'))
  else:
    print("nao encontrado")



# EXCLUIR UM PRODUTO
@login_required
def exclude_products(request, object_id):
  if request.method == "POST":
    objeto = TrackingProduct.objects.filter(object_id=object_id)
    if objeto.exists():
      group_id = request.POST.get('group_id')
      objeto.delete() 
      return redirect(f'/groupings/group/?group_id={group_id}')
    

# PARAR O MONITORAMENTO DE UM PRODUTO
def gerenciar_agrupamentos_seller(request):
  if request.method == "GET":

      
    return render(request, "groupings/gerenciar_agrupamentos_seller.html", {'agrupamentos':groups})


def getPriceVariationsGroupByAd(request):
  if request.method == 'GET':
    user = request.user
    groups = Group_by_ad.objects.filter(user=user)
    if groups.exists():
      dataJson = priceVariationsOfGroupByAd(groups)
      return JsonResponse(dataJson)

def healthVariationsOfGroupByAd(request):
  if request.method == 'GET':
    user = request.user
    groups = Group_by_ad.objects.filter(user=user)
  if groups.exists():
    dataJson = healthVariationsOfGroupByAd(groups)
    return JsonResponse(dataJson)

@login_required
def toggle_tracking_product(request, object_id):
  if request.method == "POST":
    objeto = TrackingProduct.objects.filter(object_id=object_id)
    if objeto.exists():
      print('tipo post stop')
      group_id = request.POST.get('group_id')
      product = get_object_or_404(TrackingProduct, object_id=object_id)
      current_value = product.is_tracking_activated
      product.is_tracking_activated = not current_value
      product.save()
      messages.add_message(request, constants.SUCCESS, 'O Monitoramento desse agrupamento foi alterado')
      return redirect(f'/groupings/group/?group_id={group_id}')
    else:
      print('objeto nao existe')
      return redirect(f'/groupings/group/?group_id={group_id}')
  
#Mais detalhes
def more_details(request, product_id):
  if request.method == "POST":
    print(f'ID do produto = {product_id}')
    return redirect(f'/product/?product_id={product_id}')


# def index(request, product_id):
#   if request.method == "GET":
#       app_id = config('APP_ID')
#       client_secret = config('CLIENT_SECRET')
#       refresh_token = config('REFRESH_TOKEN')
      
#       access_token = get_access_token(app_id, client_secret, refresh_token)
#       access_token = access_token["access_token"]   
#       # key_word = request.GET.get("keyWord")
#       product_id = request.GET.get("product_id")
#       # products = Product.objects.filter(Q(id=product_id) & Q(user=request.user)).all()
#       if product_id:
#           product_info = getInfoFromProduct(access_token, product_id)
#           if product_info:
      
#               return render(request, "product/index.html", {'product' : product_info})

#       return render(request, "product/index.html")

#   elif request.method == "POST":
#       return render(request, "product/index.html")
  






   




    