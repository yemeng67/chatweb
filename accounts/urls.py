from django.urls import path
from . import views
from .views import CustomLoginView

app_name = "accounts"
urlpatterns = [
    #登录界面
    path('login/',CustomLoginView.as_view() , name='login'),

    #注册界面
    path('register/', views.register_view, name='register'),

    #登出界面
    path('logout/', views.logout_view, name='logout'),
]