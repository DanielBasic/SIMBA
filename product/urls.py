from django.contrib import admin
from django.urls import path

from product.views import index


urlpatterns = [
    path("", index, name="index_product"),
]