from django.urls import path

from . import views

app_name = "post_search"
urlpatterns = [
    path('search/', views.search_index, name='search_index'),
    path('search/data/', views.search_data, name='search_data'),
]