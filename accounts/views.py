from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import RegistrationForm

import logging


def login(request):
  if request.method == "GET":
    if  request.user.is_authenticated:
      return redirect(reverse("groupByAd_management"))  
    else:
      return render(request, "registration/login.html")
  
  elif request.method == "POST":
    email_nickname = request.POST.get("email-username")
    password = request.POST.get("password")
    user_by_email = auth.authenticate(request, username=email_nickname, password=password)
    user = user_by_email
    print('entrou')
    if not user:
      user_by_nickname = User.objects.filter(email=email_nickname)
      user_by_nickname = user_by_nickname.first()
      if user_by_nickname:
        user = auth.authenticate(request, username=user_by_nickname.username, password=password)

      if not user:
        messages.add_message(request, constants.ERROR, "Email ou senha inválido")
        return redirect(reverse("login"))
    
    auth.login(request, user)
    return redirect(reverse("groupByAd_management"))
    
import json
from django.http import JsonResponse
from django.views import View


class UsernameValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    username = data['field_input']
    
    if User.objects.filter(username=username).exists():
      return JsonResponse({"field_error" : "Este apelido já está sendo usado, escolha outro"}, status=409)
    
    return JsonResponse({'field_valid' : True})
  
class EmailValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    email = data['field_input']
    
    if User.objects.filter(email=email).exists():
      return JsonResponse({"field_error" : "Este e-mail já está cadastrado, escolha outro"}, status=409)
    
    return JsonResponse({'field_valid' : True})

class PasswordValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    password = data['field_input']
    confirm_password = data['confirm_field_input']
    
    if password != confirm_password:
      return JsonResponse({"field_error" : "As senhas não conferem"}, status=400)
    
    return JsonResponse({'field_valid' : True})


def signup(request):
  if request.method == "GET":
    return render(request, "accounts/signup.html")
  
  elif request.method == "POST":
    username = request.POST.get("username")
    email =  request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    if not password == confirm_password:
      messages.add_message(request, constants.ERROR, "As senhas não conferem")
      return render(request, "accounts/signup.html")
    
    email_exists = User.objects.filter(email=email)
    username_exists = User.objects.filter(username=username)
    
    if email_exists or username_exists:
      messages.add_message(request, constants.ERROR,
                          "E-mail ou Nome já cadastrado")
      return render(request, "accounts/signup.html")

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso")
    
    return redirect(reverse("login")) 
  


def register(request): 
  if request.method == "POST":
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      mensagem = "Usuario criado com sucesso"
      context = {
        'mensagem' : mensagem,
      }
      return render(request, "registration/login.html", context)
    else:
      mensagem = "Dados invalidos"
      context = {
        'form' : form,
        'mensagem' : mensagem,

      }
      return render(request, "accounts/register.html", context)
  
  else:
    form = RegistrationForm()
    context = {
      'form' : form
    }
    return render(request, "accounts/register.html", context)

    






def logout(request):
  auth.logout(request)
  return redirect(reverse("login"))
    



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

def sobre(request):
  if request.method == "GET":
    return render(request, "accounts/sobre.html")


def usuario(request):
  if request.method == "GET":
    return render(request, "accounts/usuario.html")
  
  

def update_profile(request):
  if request.method == 'POST':
    new_username = request.POST['username']
    new_email = request.POST['email']
    # new_password = request.POST.get("password")
    # new_confirm_password = request.POST.get("confirm_password")


    user = request.user
    user.username = new_username
    user.email = new_email  
    # user.password = new_password
    # user.confirm_password = new_confirm_password


    try:
      user.save()
      messages.success(request, 'Perfil atualizado com sucesso!')
      return render(request, "accounts/usuario.html")
    except Exception as e:
        messages.error(request, f"Erro ao atualizar perfil usuario ou email ja utilizados")

    return render(request, "accounts/usuario.html")
  

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash  

def alterar_senha(request):
  
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)
    if form.is_valid():
      form.save()
      update_session_auth_hash(request, form.user)
      messages.success(request, 'Perfil atualizado com sucesso!')
      return render(request, "accounts/usuario.html")
    else:
      messages.error(request, f"Erro ao atualizar perfil:")
      return render(request, "accounts/usuario.html")
      
  else:
    messages.error(request, f"Erro ao atualizar perfil:")
    form = PasswordChangeForm(user=request.user)
    context = {
      'form' : form
    }
    messages.error(request, "Erro ao atualizar perfil:")
    return render(request, "accounts/usuario.html")

    

    
  

