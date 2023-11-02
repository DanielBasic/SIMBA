from django.contrib import admin
from django.urls import path

from .views import index, details_product
from . import views


urlpatterns = [
    path("", index, name="index_product"),

]