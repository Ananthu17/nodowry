from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from dashboard.models import *
from django.urls import reverse


class HomePage(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['religion_list'] = Religion.objects.all()
        context['language_list'] = MotherTongue.objects.all()
        return context


class QuickFilter(TemplateView):
    template_name = 'frontend/filterscreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gender = self.request.GET.get('gender')
        agefrom = self.request.GET.get('agefrom')
        ageto = self.request.GET.get('ageto')
        religion_id = self.request.GET.get('religion')
        language = self.request.GET.get('language')
        print(gender)
        print(agefrom)
        print(ageto)
        print(religion_id)
        print(language)
        userprofile = UserProfile.objects.filter(is_active=True, gender=gender, userinfo__religion=religion_id, userinfo__mother_tongue=language).values('user__first_name', 'userinfo__userimages__file', 'userinfo__dob')
        context['user_profile'] = userprofile
        context['user_count'] = userprofile.count()
        return context


class ConfirmYourEmail(TemplateView):
    template_name = 'frontend/confirm-your-email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context