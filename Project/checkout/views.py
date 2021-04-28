from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAVE_PUBLIC_KEY
        return context

class Success(TemplateView):
    template_name = 'success.html'

class Failure(TemplateView):
    template_name = 'failure.html'