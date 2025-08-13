# Main URLs Configuration for pipsmade Investment Platform
# This goes in your main pipsmade_backend/urls.py file

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # Authentication URLs
    path('', include('accounts.urls')),  # login, signup, logout, profile
    
    # Dashboard URLs
    path('dashboard/', include('dashboard.urls')),
    
    # Investment URLs
    path('investments/', include('investments.urls')),
    
    # Transaction URLs
    path('transactions/', include('transactions.urls')),
    
    # Support URLs
    path('support/', include('support.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Example accounts/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
"""

# Example dashboard/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
]
"""

# Example investments/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.investments_view, name='investments'),
    path('create/', views.create_investment_view, name='create_investment'),
    path('<int:investment_id>/', views.investment_detail_view, name='investment_detail'),
]
"""

# Example transactions/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_history_view, name='transactions'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
]
"""

# Example support/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_view, name='support'),
    path('ticket/create/', views.create_ticket_view, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
"""
