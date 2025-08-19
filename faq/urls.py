from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_list, name='faq_list'),
    path('category/<slug:category_slug>/', views.faq_by_category, name='faq_by_category'),
] 