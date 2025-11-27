from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


# 登录视图
# @csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blindbox:blindbox')  # 登录成功后跳转到盲盒页面
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 注册视图
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # 注册成功后跳转到登录页面
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
