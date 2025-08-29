from django.urls import path
from . import views

app_name = 'crypto_news'

urlpatterns = [
    path('', views.CryptoNewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', views.CryptoNewsDetailView.as_view(), name='news_detail'),
]
