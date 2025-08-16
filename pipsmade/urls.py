from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HomeView, AboutView, ContactView, health_check, test_static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('alert-demo/', TemplateView.as_view(template_name='alert_demo.html'), name='alert_demo'),
    path('health/', health_check, name='health_check'),
    path('test-static/', test_static, name='test_static'),

    # Authentication URLs
    path('', include('accounts.urls')),

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
else:
    # In production, serve static files
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

