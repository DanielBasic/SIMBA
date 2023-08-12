from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

# Create your views here.

def gerenciar_agrupamentos(request):
  if request.method == "GET":
    return render(request, "groupings/gerenciar_agrupamentos.html")
  
def criar_agrupamentos(request):
  if request.method == "GET":
    return render(request, "groupings/criar_agrupamentos.html")

