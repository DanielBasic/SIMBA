from django.urls import path

from . import views

urlpatterns = [
  path("gerenciar_agrupamentos_produtos/", views.gerenciar_agrupamentos_produtos, name="gerenciar_agrupamentos_produtos"),
  path("criar_agrupamentos_produtos/", views.criar_agrupamentos_produtos, name="criar_agrupamentos_produtos"),
  path("gerenciar_agrupamentos_seller/", views.gerenciar_agrupamentos_seller, name="gerenciar_agrupamentos_seller"),
  path("criar_agrupamentos_seller/", views.criar_agrupamentos_seller, name="criar_agrupamentos_seller"),
]