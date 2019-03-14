from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from MainApp import forms
from MainApp import tools
from MainApp.tools import send_mail
from concurrent.futures import ThreadPoolExecutor
import zipfile
import os


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

    args = {'message': '', 'form': forms.ArchiveUploadForm,
            'detection_objects': tools.objs_labels()}

    if request.method == 'POST':
        tools.send_mail('tzmakoev@edu.hse.ru')
        form = forms.ArchiveUploadForm(request.POST, request.FILES)

        objs_to_detect = []
        labels = tools.objs_labels()
        for key in request.POST.keys():
            if key in labels:
                objs_to_detect.append(key)

        if not form.is_valid(request.FILES.keys()):
            args['message'] = 'load zip archive'
        else:
            # process
            file = request.FILES['archive']
            file_name = str(file)
            is_zip = tools.is_zip(file_name)
            is_image = tools.is_image(file_name)
            if not is_zip and not is_image:
                args['message'] = 'it is not a zip or a single image file'
            elif is_zip:
                zips_folder_path = 'files/zips/'
                email = request.user.email
                title = tools.get_unique_title()
                zip_file_name = email + '_' + title
                zip_abs_path = zips_folder_path + zip_file_name + '.zip'
                fout = open(zip_abs_path, 'wb+')
                for chunk in file.chunks():
                    fout.write(chunk)
                fout.close()
                ex = ThreadPoolExecutor(max_workers=1)
                future = ex.submit(tools.processing, zip_file_name, objs_to_detect)
                args['message'] = 'we will send you an email to {} with detection result'.format(email)
            elif is_image:
                zips_folder_path = 'files/zips/'
                email = request.user.email
                title = tools.get_unique_title()
                img_file_name = email + '_' + title
                img_abs_path = zips_folder_path + img_file_name + '.jpg'
                fout = open(img_abs_path, 'wb+')
                for chunk in file.chunks():
                    fout.write(chunk)
                fout.close()
                zip_abs_path = zips_folder_path + img_file_name + '.zip'
                zip_ref = zipfile.ZipFile(zip_abs_path, 'w')
                zip_ref.write(img_abs_path, file_name)
                zip_ref.close()
                os.remove(img_abs_path)
                ex = ThreadPoolExecutor(max_workers=1)
                future = ex.submit(tools.processing, img_file_name, objs_to_detect)
                args['message'] = 'we will send you an email to {} with detection result'.format(email)
    return render(request, 'MainApp/home.html', args)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('login')


def info(request):
    return render(request, 'MainApp/info.html')










