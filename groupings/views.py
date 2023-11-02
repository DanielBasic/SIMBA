from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import GroupByAd_form
from api_MercadoLivre.getContent import str_to_dict
from django.db.models import Q
from django.core.files.base import ContentFile
from product.models import Product, TrackingProduct
from .models import Group_by_ad
from product.tasks import add_geral_infos_product_in_db
from .utils import add_products_into_group
import os


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
      groupByAd = Group_by_ad(image=image, title=title, user=request.user)
      groupByAd.save()
      messages.add_message(request, constants.SUCCESS,'Agrupamento criado com sucesso')
      return redirect(reverse('groupByAd_management'))

    messages.add_message(request, constants.ERROR, 'Adicione uma imagem e um título válido')                      
    return redirect(reverse('groupByAd_management'))
  

    
@login_required
def groupByAd_management(request):
  if request.method == "GET":
    groupByAd_all = Group_by_ad.objects.filter(user=request.user)
    form_groupByAd = GroupByAd_form()
    return render(request, "groupings/groupByAd_management.html", {'groupByAd_all': groupByAd_all , 'groupByAd_form' : form_groupByAd})


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
        print(f'products ids: {list(products_id.keys())}')
        add_geral_infos_product_in_db.delay(products_id)
        if product_already_in_group:
          messages.add_message(request, messages.ERROR , f'Não foi possível adicionar os seguinte produtos, pois eles já estão adicionados nesse agrupamento: {product_already_in_group}')
        else:
          messages.add_message(request, messages.SUCCESS,'Monitoramento iniciado com sucesso')
      return redirect(f"/groupings/group/?group_id={group.id}")
    except ValueError as e:
      print(f"Error at add_products_into_GroupByAd: {e}")
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
          messages.error(request, f'O grupo com título {title} já existe.')
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
    else:
      raise TypeError("The group_id must be a int type")
    return render(request, "groupings/groupByAd_details.html", {'products' : products})


# PARAR O AGRUPAMENTO
@login_required
def stop_groupByAd(request, group_id):
    if request.method == "GET":
      group = get_object_or_404(Group_by_ad, id=group_id)
      group.is_tracking_activated
      return render(request, 'groupByAd_management.html', group.is_tracking_activated)
    
    if request.method == "POST":
        group = get_object_or_404(Group_by_ad, id=group_id)
        current_value = group.is_tracking_activated
        group.is_tracking_activated = not current_value
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

         
# EXCLUIR UM AGRYUPAMENTO
@login_required
def exclud_groupByAd(request, group_id):
  if request.method == "POST":
    objeto = Group_by_ad.objects.filter(id=group_id)
    if objeto.exists():
      objeto.delete()
     
      return redirect(reverse('groupByAd_management'))
  else:
    print("nao encontrado")