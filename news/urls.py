from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('categoria/<slug:category_slug>/', views.NewsListView.as_view(), name='news_by_category'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]
