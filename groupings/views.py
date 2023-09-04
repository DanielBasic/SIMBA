from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import GroupByAd_form
from api_MercadoLivre.getContent import str_to_dict
from product.models import Product
from django.db.models import Q

from .models import Group_by_ad

# Create your views here.

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
      user_products = Product.objects.filter(user=current_user)


      if products and group:
        productsAlreadyIntoTheGroup = []
        for product in products:
          id, price, seller = product['id'], product['price'].replace(',', '.'), product["sellerId"]
          db_product = user_products.filter(Q(id=id) & Q(group=group)).first()
          if db_product:
            productsAlreadyIntoTheGroup.append(id)
          else:
            product_object = Product(id=id,
                                      price=price,
                                            seller=seller)
            product_object.save()
            product_object.user.add(current_user)
            product_object.group.add(group)
      messages.info(request, f'Não foi possível adicionar os seguinte produtos, pois eles já estão adicionados nesse agrupamento: {productsAlreadyIntoTheGroup}')

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

      if products and group:
        for product in products:
          id, price, seller = product['id'], product['price'].replace(',', '.'), product["sellerId"]
          product_object = Product(id=id,
                                    price=price,
                                          seller=seller)
          product_object.save()
          product_object.user.add(current_user)
          product_object.group.add(group)
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
      products = Product.objects.filter(Q(user=user) & Q(group=group))
    else:
      raise TypeError("The group_id must be a int type")
    return render(request, "groupings/groupByAd_details.html", {'products' : products})


@login_required
def deletar_agrupamentos(request):
  pass
  
@login_required
def gerenciar_agrupamentos_seller(request):
  if request.method == "GET":
    grupos = Group_by_ad.objects.filter(user=request.user)
    return render(request, "groupings/gerenciar_agrupamentos_seller.html", {'agrupamentos':grupos })

@login_required
def criar_agrupamentos_seller(request):
  if request.method == "GET":
    return render(request, "groupings/criar_agrupamentos_seller.html")
  elif request.method == "POST":
    logo = request.POST.get("logo")
    name  = request.POST.get("title")
    start_date  = request.POST.get("start_date")
    description  = request.POST.get("description")
    # agrupamento_seler = Agrupamento_seller(
    #   criador=request.user,
    #   logo = logo,
    #   name = name,
    #   start_date = start_date,
    #   description = description, 
    # )
    # agrupamento_seler.save()

    messages.add_message(request, constants.SUCCESS,'Evento cadastrado com sucesso')
                            
    return redirect(reverse('create_new_groupByAd'))