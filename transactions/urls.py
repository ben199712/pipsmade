from django.urls import path
from . import views

urlpatterns = [
    path('', views.transactions_view, name='transactions'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    
    # Admin URLs
    path('admin/', views.admin_transactions, name='admin_transactions'),
    path('admin/deposit/<int:deposit_id>/approve/', views.admin_approve_deposit, name='admin_approve_deposit'),
    path('admin/withdrawal/<int:withdrawal_id>/process/', views.admin_process_withdrawal, name='admin_process_withdrawal'),
    
    # Notification URLs
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
