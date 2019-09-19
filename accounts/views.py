from django.shortcuts import render
from django.views.generic import View, TemplateView


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
