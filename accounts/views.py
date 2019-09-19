from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
            name = request.POST.get('name', "")
            password = request.POST.get('password', "")
            email = request.POST.get('email', "")

            if email is not None:
                if not User.objects.filter(username=email):
                    try:
                        user = User.objects.create_user(username=email, firstname = name, email=email, password=password)
                        user.save()
                        return redirect('home')
                    except:
                        return redirect('home')
                return redirect('home')
            return redirect('home')


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
