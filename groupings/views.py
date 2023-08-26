from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Group_by_ad

# Create your views here.

@login_required
def criar_agrupamentos_produtos(request):
  if request.method == "GET":
    return render(request, "groupings/criar_agrupamentos_produtos.html")
  elif request.method == "POST":
    logo = request.POST.get("logo")
    title  = request.POST.get("title")
    start_date  = request.POST.get("start_date")
    description  = request.POST.get("description")

    agrupamento = Group_by_ad(
      criador=request.user,
      logo = logo,
      title = title,
      start_date = start_date,
      description = description, 
    )
    agrupamento.save()

    messages.add_message(request, constants.SUCCESS,'Evento cadastrado com sucesso')
                            
    return redirect(reverse('criar_agrupamentos_produtos'))
  

    
@login_required
def gerenciar_agrupamentos_produtos(request):
  if request.method == "GET":
    grupos = Group_by_ad.objects.filter(criador=request.user)
    return render(request, "groupings/gerenciar_agrupamentos_produtos.html", {'agrupamentos':grupos })


def deletar_agrupamentos(request):
  pass
  

def gerenciar_agrupamentos_seller(request):
  if request.method == "GET":
    grupos = Group_by_ad.objects.filter(criador=request.user)
    return render(request, "groupings/gerenciar_agrupamentos_seller.html", {'agrupamentos':grupos })


def criar_agrupamentos_seller(request):
  pass

