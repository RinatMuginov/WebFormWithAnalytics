from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == 'register':
            return redirect('register')

        elif action == 'login':
            username = request.POST.get('user_login').strip()
            password = request.POST.get('user_password').strip()

            if not username or not password:
                messages.error(request, 'Заполните все поля!')
                return redirect('login')

            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль!')
                return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == 'register':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email').strip()
            username = request.POST.get('user_login').strip()
            password = request.POST.get('user_password')
            password_confirmation = request.POST.get('password_confirmation')
            fields = [first_name, last_name, email, username, password]

            if all(field for field in fields) == False:
                messages.error(request, 'Заполните все поля!')
                return redirect('register')
            
            elif User.objects.filter(email=email):
                messages.error(request, 'Пользователь с такой почтой уже существует!')
                return redirect('register')
            
            elif User.objects.filter(username=username):
                messages.error(request, 'Пользователь с таким логином уже существует!')
                return redirect('register')
            
            elif password != password_confirmation:
                messages.error(request, 'Пароли не совпадают')
                return redirect('register')

            else:
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                return redirect('login')


    return render(request, 'register.html')

def home_view(request):
    return render(request, 'success.html')