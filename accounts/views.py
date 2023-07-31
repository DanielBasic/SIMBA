from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .admin import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('mysite')

        else:
            print('invalid registration details')
            
    return render(request, "registration/register.html",{"form": form})
  
def login(request):
  if request.method == "GET":
    return render(request, "accounts/login.html")
  
  elif request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = auth.authenticate(request, email=email, password=password)

    if not user:
      messages.add_message(request, constants.ERROR, "Email ou senha inválido")
      return redirect(reverse("login"))

    messages.add_message(request, constants.SUCCESS,"Logado com sucesso")
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
    
    user = User.objects.filter(username=username)

    if user.exists():
      messages.add_message(request, constants.ERROR,
                          "username ja Cadastrado")
      return render(request, "accounts/signup.html")


    user = User.objects.filter(email=email)
    
    if user.exists():
      messages.add_message(request, constants.ERROR,
                          "E-mail já cadastrado")
      return render(request, "accounts/signup.html")
    
    user = User.objects.create_user(username=username, email=email, password=password)

    messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso")
    
    return redirect(reverse("login"))
  

def logout(request):
  auth.logout(request)
  messages.success(request, 'Logout efetuado com sucesso!')
  return redirect('login')
    

def sobre(request):
  if request.method == "GET":
    return render(request, "accounts/sobre.html")


  

