from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            auth_login(request, data)
            return redirect('chat:chat_panel')
        else:
            print(111111)
            context = {'form': form}
            print(form)
            return render(request, 'user_mgmt/login.html', context)
    elif request.method == "GET":
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'user_mgmt/login.html', context)
    else:
        return render(request, "404.html")

def user_register(request):
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、联系方式（telphone）、性别（gender）、年龄（age）
        # 用这些数据实例化一个用户注册表单
        user_register_form = UserRegisterForm(request.POST)

        # 验证数据的合法性
        if user_register_form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            register_data = user_register_form.cleaned_data
            register_data.pop("password1")
            obj = UserTbl(**register_data)
            obj.save()
            # 注册成功，跳转登录
            return redirect('user_mgmt:auth_login')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        user_register_form = UserRegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'user_mgmt/register.html', context={'form': user_register_form})



def auth_login(request, data):
    username = data.get('username')
    password = data.get('password')
    user = UserTbl.objects.filter(username=username)
    if user.exists():
        if password == user.first().password:
            request.session['user_id'] = username


def auth_logout(request):
    try:
        del request.session['user_id']
    except KeyError as e:
        print("logout error")
        print(e)
    finally:
        return redirect('user_mgmt:auth_login')


def login_required(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_id'):
            request.session.set_expiry(60*10)
            function = func(request,*args, **kwargs)
            return function
        else:
            return redirect('user_mgmt:auth_login')

    return inner
