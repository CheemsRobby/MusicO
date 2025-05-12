from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.http import JsonResponse
import os

def index(request):
    return render(request, 'index.html')

def upload_music(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        music_file = request.FILES.get('music_file')

        if title and artist and music_file:
            # 保存文件到指定目录
            upload_dir = os.path.join(os.getcwd(), 'music_uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, music_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in music_file.chunks():
                    destination.write(chunk)
            # 修正：使用reverse或直接URL名称
            return redirect('upload_music' + '?success=true')
        else:
            # 修正：使用reverse或直接URL名称
            return redirect('upload_music' + '?success=false')

    return render(request, 'upload_music.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
def index(request):
    return render(request, 'index.html')

def upload_music(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        music_file = request.FILES.get('music_file')

        if title and artist and music_file:
            # 保存文件逻辑
            upload_dir = os.path.join(os.getcwd(), 'music_uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, music_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in music_file.chunks():
                    destination.write(chunk)
            return redirect('upload_music' + '?success=false')
        else:
            return redirect('upload_music' + '?success=false')

    return render(request, 'upload_music.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if role == 'admin':
            user = User.objects.create_superuser(username=username, email=email, password=password)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

        if user:
            messages.success(request, '注册成功，请登录')
            return redirect('login')
        else:
            messages.error(request, '注册失败，请重试')

    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('index')
