from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse


def login(request):
  if request.method == "GET":
    return render(request, "registration/login.html")
  
  elif request.method == "POST":
    email_nickname = request.POST.get("email-username")
    password = request.POST.get("password")
    user = auth.authenticate(request, username=email_nickname, password=password)

    if not user:
      user_by_nickname = User.objects.filter(email=email_nickname)
      user_by_nickname = user_by_nickname.first()
      if user_by_nickname:
        user = auth.authenticate(request, username=user_by_nickname.username, password=password)
      if not user:
        messages.add_message(request, constants.ERROR, "Email ou senha inválido")
        return redirect(reverse("login"))
    
    
    auth.login(request, user)

    return redirect(reverse("search"))
    

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

def logout(request):
  auth.logout(request)
  return redirect(reverse("login"))
    

def sobre(request):
  if request.method == "GET":
    return render(request, "accounts/sobre.html")
