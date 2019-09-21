from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.models import UserProfile
from django.contrib import messages
import copy
from django.core.mail import send_mail
from twilio.rest import Client
from random import randint


account_sid = 'AC96e8076569e146b9592cfc8ac8502f6b'
auth_token = '63afcb2adddfa49991e700964be7bd5e'
client = Client(account_sid, auth_token)


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
            name = request.POST.get('name', "")
            password = request.POST.get('password', "")
            email = request.POST.get('email', "")
            phone_number = request.POST.get('mobno', "")
            code = str(randint(1000, 9999))
            email_content = "You are successfully registered. Thank you for choosing us."

            send_mail(
                'Thank you for registering',
                email_content,
                'matrimonyapp@gmail.com',
                [email],
                html_message=email_content,
                fail_silently=False
            )
            # messagetext = str(code) + " Is the OTP for NoDowry Martimony.NEVER SHARE YOUR OTP WITH ANYONE"
            message = client.messages.create(
                body= code + " Is the OTP for NoDowry Martimony.NEVER SHARE YOUR OTP WITH ANYONE",
                from_='+12055836771',
                to='+91' + phone_number
            )

            print(message.sid)

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

                    except User.DoesNotExist:
                        messages.error(request, "cannot able to create new user")
                        return redirect('register')
                else:
                    messages.error(request, "user is already exists")
                    return redirect('register')
            else:
                messages.error(request, "Username and password is not valid")
                return redirect(reverse('register'))


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

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
                user_profile = UserProfile.objects.get(user=user)
                if not user.is_superuser:
                    if user_profile.is_active:
                        if user.check_password(password):
                            login(request, user)
                            return redirect(reverse('home'))
                        else:
                            messages.error(request, "Invalid Credentials")
                            return redirect(reverse('login'))
                    else:
                        messages.error(request, "profile is blocked, Please contact admin")
                        return redirect(reverse('login'))
                else:
                    messages.error("Invalid Credentials")
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials, Please try again")
                return redirect(reverse('login'))
        else:
            messages.error(request, "Username and password is not valid")
            return redirect(reverse('login'))


class LogOut(LoginRequiredMixin, View):
    """
    View for logging out user and redirect to login page
    """
    def get(self, request):
        user = copy.deepcopy(request.user)
        if request.user.is_authenticated:
            logout(request)
            messages.error(request, "You have been logged out. Hope you will be back soon.")
        return redirect(reverse('login'))

