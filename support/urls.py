from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class SupportView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/support.html'

urlpatterns = [
    path('', SupportView.as_view(), name='support'),
]
