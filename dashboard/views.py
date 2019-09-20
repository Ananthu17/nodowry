from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import View, TemplateView
from datetime import datetime
from .models import *
import copy


class DashboardLogIn(TemplateView):
    template_name = 'dashboard/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        """
        :param request:
        :username:Username
        :password:Password
        """
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username != "" and password != "":
            try:
                user = User.objects.get(username=username)
                if user.is_superuser:
                    if user.is_active:
                        if user.check_password(password):
                            login(request, user)
                            return redirect(reverse('dashboard'))
                        else:
                            messages.error(request, "Invalid Credentials")
                            return redirect(reverse('dashboard-login'))
                    else:
                        messages.error(request, "profile is not active, Please contact admin")
                        return redirect(reverse('dashboard-login'))
                else:
                    messages.error("Invalid Credentials")
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials, Please try again")
                return redirect(reverse('dashboard-login'))
        else:
            messages.error(request, "Username and password is not valid")
            return redirect(reverse('dashboard-login'))


class DashboardLogOut(LoginRequiredMixin, View):
    """
    View for logging out user and redirect to login page
    """
    def get(self, request):
        user = copy.deepcopy(request.user)
        if request.user.is_authenticated:
            logout(request)
            messages.error(request, "You have been logged out. Hope you will be back soon.")
        return redirect(reverse('dashboard-login'))


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, *args, **kwargs):

        first_date = self.request.GET.get("start_date", "")
        last_date = self.request.GET.get("end_date", "")
        context = super().get_context_data(**kwargs)
        user_count = UserProfile.objects.all().count()
        deactivated_user_count = UserProfile.objects.filter(is_active=False).count()
        new_users = 0
        if first_date and last_date:
            new_users = UserProfile.objects.filter(created_at__range=(first_date, last_date)).count()
        else:
            end_date = datetime.today()
            start_date = datetime(end_date.year, end_date.month, 1)
            new_users = UserProfile.objects.filter(created_at__range=(start_date, end_date)).count()

        context['user_count'] = user_count
        context['deactivated_user_count'] = deactivated_user_count
        context['new_users'] = new_users
        return context


class DashboardUsers(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = UserProfile.objects.all()
        context['user_list'] = user_list
        return context

