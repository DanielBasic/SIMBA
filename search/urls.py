from django.urls import path

from . import views

urlpatterns = [
  path("", views.search, name="search"),
  path("add_products_group_by", views.track_products, name='add_products_group_by'),
  path('add_product/', views.add_product, name='add_product'),
  


]
