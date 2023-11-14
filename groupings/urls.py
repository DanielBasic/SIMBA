from django.urls import path

from . import views

urlpatterns = [
  path("groupByAd_management/", views.groupByAd_management, name="groupByAd_management"),
  path("create_new_groupByAd/", views.create_new_groupByAd, name="create_new_groupByAd"),
  # path("gerenciar_agrupamentos_seller/", views.gerenciar_agrupamentos_seller, name="gerenciar_agrupamentos_seller"),
  # path("criar_agrupamentos_seller/", views.criar_agrupamentos_seller, name="criar_agrupamentos_seller"),
  path("add_products_into_GroupByAd/", views.add_products_into_GroupByAd, name="add_products_into_GroupByAd"),
  path("create_new_GroupByAd_addProductsInIt/", views.create_new_GroupByAd_addProductsInIt, name="create_new_GroupByAd_addProductsInIt"),
  path("group/", views.groupByAd_details, name="groupByAd_details"),


  path('toggle_tracking_groupByAd/<int:group_id>/', views.toggle_tracking_groupByAd, name='toggle_tracking_groupByAd'),
  path('edit_groupByAd/', views.edit_groupByAd, name='edit_groupByAd'),
  path('exclude_groupByAd/<int:group_id>/', views.exclude_groupByAd, name='exclude_groupByAd'),

  path('exclude_products/<int:object_id>/', views.exclude_products, name='exclude_products'),
  path('toggle_tracking_product/<int:object_id>/', views.toggle_tracking_product, name='toggle_tracking_product'),
  path('more_details/<str:product_id>/', views.more_details, name='more_details'),

  path('getPriceVariationsGroupByAd/', views.getPriceVariationsGroupByAd, name='getPriceVariationsGroupByAd'),
  path('healthVariationsOfGroupByAd/', views.healthVariationsOfGroupByAd, name='healthVariationsOfGroupByAd')


]