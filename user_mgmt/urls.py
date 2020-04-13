from django.urls import path
from . import views

app_name = "user_mgmt"
urlpatterns =[
    path('login',views.user_login,name="auth_login"),
    path('logout',views.auth_logout,name="auth_logout"),
]