from django.urls import path

from . import views

urlpatterns = [
  path("gerenciar_agrupamentos/", views.gerenciar_agrupamentos, name="gerenciar_agrupamentos"),
  path("criar_agrupamentos/", views.criar_agrupamentos, name="criar_agrupamentos"),
  
]