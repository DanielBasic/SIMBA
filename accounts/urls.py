
from django.urls import path
from . import views

urlpatterns = [
  path("login/", views.login, name="log_in"),
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout, name="logout"),
  path("sobre/", views.sobre, name="sobre"),
]