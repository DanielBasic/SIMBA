from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
  path("", views.login, name="login"),
  path("novo_login/", views.novo_login, name="novo_login"),
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout, name="logout"),
  path("rota_teste/", views.rota_teste, name="rota_teste"),
  path("sobre/", views.sobre, name="sobre"),
  path("novo_signup/", views.novo_signup, name="novo_signup"),

]