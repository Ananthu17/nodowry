from django.views.generic import View, TemplateView
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.models import UserProfile


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
                        user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
                        user.save()
                        gender = request.POST.get('gender', "")
                        phone_number = request.POST.get('mobno', "")
                        dob = request.POST.get('dob', "")
                        lang_id = request.POST.get('language', "")
                        # mother_tongue = MotherTongue.objects.get(id=lang_id)
                        print(gender+" "+phone_number+" "+dob+" "+lang_id)
                        userprofile_obj = UserProfile(
                                                user=user,
                                                gender=gender,
                                                phone_number=phone_number,
                                                is_user=True)
                        userprofile_obj.save()
                        return redirect('home')
                    except:
                        return redirect('login')
                return redirect('register')
            return redirect('home')


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
