from django.urls import path
from . import views

urlpatterns = [
  path("search", views.search, name="search"),
  path('add_product/', views.add_product, name='add_product'),
  path('gerenciar_agrupamento/', views.gerenciar_agrupamento, name='gerenciar_agrupamento'),

]
