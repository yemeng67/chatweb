from django.urls import path
from . import views

app_name = "userspace"
urlpatterns = [
    path('index/', views.index, name='index'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('update_bio/', views.update_bio, name='update_bio'),

]