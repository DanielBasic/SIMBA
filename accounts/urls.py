from django.conf.urls.static import static
from django.urls import path

from accounts import views

from . import views

urlpatterns = [
  path("login/", views.login, name="login"),
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout, name="logout"),
  path("sobre/", views.sobre, name="sobre"), 
  path('register/', views.register, name='register'),
]