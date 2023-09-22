from django.urls import path

from . import views

urlpatterns = [
  path("", views.search, name="search"),
  path('add_product/', views.add_product, name='add_product'),
  path('async/', views.teste_async, name='async')
]
