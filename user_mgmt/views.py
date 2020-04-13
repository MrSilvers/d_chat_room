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
            function = func(request,*args, **kwargs)
            return function
        else:
            return redirect('user_mgmt:auth_login')

    return inner
