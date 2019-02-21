from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    data = {'message': ''}
    if request.method == 'POST':
        user_login = request.POST['email']
        user_password = request.POST['password']
        if user_login == '' or user_password == '':
            data['message'] = 'Enter all fields'
        else:
            user = auth.authenticate(username=user_login, password=user_password)
            if user is None:
                data['message'] = 'No such user'
            else:
                auth.login(request, user)
                return redirect('home')
    return render(request, 'MainApp/login.html', data)


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    data = {'message': ''}
    if request.method == 'POST':
        user_login = request.POST['email']
        user_password = request.POST['password']
        user_confirm = request.POST['password_confirmation']
        if user_login == '' or user_password == '' or user_confirm == '':
            data['message'] = 'Enter all fields.'
        elif User.objects.check(username=user_login):
            data['message'] = 'Such user exists.'
        elif user_password != user_confirm:
            data['message'] = 'Passwords are different.'
        else:
            user = User.objects.create_user(username=user_login, email=user_login, password=user_password)
            user.save()
            user = auth.authenticate(username=user_login, password=user_password)
            auth.login(request, user)
            return redirect('home')
    return render(request, 'MainApp/signup.html', data)


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'MainApp/home.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('login')










