from django.shortcuts import render
from django.views.generic import View, TemplateView
from datetime import datetime
from .models import *


class Dashboard(TemplateView):
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

class DashboardUsers(TemplateView):
    template_name = 'dashboard/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = UserProfile.objects.all()
        context['user_list'] = user_list
        return context
