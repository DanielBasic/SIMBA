from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
  path("", views.login, name="login"),
  path("novo_login/", views.novo_login, name="novo_login"),
  path("signup/", views.signup, name="signup"),
] 