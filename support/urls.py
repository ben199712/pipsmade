from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # Main support pages
    path('', views.support_center, name='support_center'),
    path('tickets/', views.my_tickets, name='my_tickets'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    # Knowledge base and FAQs
    path('kb/', views.knowledge_base, name='knowledge_base'),
    path('kb/<slug:slug>/', views.article_detail, name='article_detail'),
    path('faq/', views.faq_list, name='faq_list'),

    # Search and quick support
    path('search/', views.search_support, name='search_support'),
    path('quick-help/', views.quick_help, name='quick_help'),

    # AJAX endpoints
    path('api/search/', views.ajax_search, name='ajax_search'),
    path('api/ticket/<int:ticket_id>/close/', views.ajax_close_ticket, name='ajax_close_ticket'),
]
