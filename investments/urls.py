from django.urls import path
from . import views

urlpatterns = [
    path('', views.investments_view, name='investments'),
    path('create/', views.create_investment, name='create_investment'),
    path('<int:investment_id>/', views.investment_detail, name='investment_detail'),
    path('<int:investment_id>/cancel/', views.cancel_investment, name='cancel_investment'),
    path('calculator/', views.investment_calculator, name='investment_calculator'),
]
