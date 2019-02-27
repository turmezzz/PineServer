from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from . import forms
from . import tools



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
        elif User.objects.filter(username=user_login).exists():
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

    args = {'message': '', 'form': forms.ArchiveUploadForm}
    if request.method == 'POST':
        form = forms.ArchiveUploadForm(request.POST, request.FILES)
        if not form.is_valid(request.FILES.keys()):
            args['message'] = 'load zip archive'
        else:
            # process
            file = request.FILES['archive']
            file_name = str(file)
            if not tools.is_zip(file_name):
                args['message'] = 'it is not a zip file'
            else:
                zips_folder_path = 'files/zips/'
                email = request.user.email
                time = tools.get_unique_title()
                zip_file_name = zips_folder_path + email + '_' + time + '.zip'
                fout = open(zip_file_name, 'wb+')
                for chunk in file.chunks():
                    fout.write(chunk)
                fout.close()
                return HttpResponse('We will send email')
    return render(request, 'MainApp/home.html', args)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('login')


def info(request):
    return render(request, 'MainApp/info.html')










