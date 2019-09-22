from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.models import UserProfile
from django.contrib import messages
from django.template import loader
import copy
from django.core.mail import send_mail, EmailMultiAlternatives
from twilio.rest import Client
import random
from random import randint
import hashlib
import datetime
from django.utils import timezone

from django.template.loader import render_to_string


# twillo services tocken
account_sid = 'AC96e8076569e146b9592cfc8ac8502f6b'
auth_token = '63afcb2adddfa49991e700964be7bd5e'
client = Client(account_sid, auth_token)


def send_confirmation_email(context):
    email = context['email']
    template = loader.get_template("accounts/email_confirmation.html")
    email_content = template.render(context)
    send_mail(
        'NoDowry Email verification',
        email_content,
        'help@nodowry.com',
        [email],
        html_message=email_content,
        fail_silently=False
    )


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
            # email_content = "You are successfully registered. Thank you for choosing us."
            #
            # send_mail(
            #     'Thank you for registering',
            #     email_content,
            #     'matrimonyapp@gmail.com',
            #     [email],
            #     html_message=email_content,
            #     fail_silently=False
            # )
            # # messagetext = str(code) + " Is the OTP for NoDowry Martimony.NEVER SHARE YOUR OTP WITH ANYONE"

            '''
            Sending otp for the users
            '''
            # message = client.messages.create(
            #     body= code + " Is the OTP for NoDowry Martimony.NEVER SHARE YOUR OTP WITH ANYONE",
            #     from_='+12055836771',
            #     to='+91' + phone_number
            # )
            # print(message.sid)

            if email is not None:
                if not User.objects.filter(username=email):
                    try:
                        user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
                        user.save()
                        '''
                        We generate a random activation key
                        '''
                        usernamesalt = email
                        activation_key = hashlib.sha256((str(random.getrandbits(256)) + usernamesalt).encode('utf-8')).hexdigest()
                        activation_key_expiry = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")

                        '''
                        creating the mail confirmation url
                        '''
                        context = {}
                        context['activation_key'] = activation_key
                        context['email'] = email
                        context['name'] = name
                        context['email_confirmation_url'] = request.scheme + "://" + request.META["HTTP_HOST"] + reverse(
                            'user-email-verification', kwargs={'email': email, 'activation_key': activation_key})

                        '''
                        sending verification mail to the user
                        '''
                        send_confirmation_email(context)

                        gender = request.POST.get('gender', "")
                        phone_number = request.POST.get('mobno', "")
                        dob = request.POST.get('dob', "")
                        userprofile_obj = UserProfile(
                                                user=user,
                                                gender=gender,
                                                phone_number=phone_number,
                                                is_user=True,
                                                is_active=False,
                                                activation_key=activation_key,
                                                key_expires=activation_key_expiry
                                                )
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


class EmailConfirmation(TemplateView):
    template_name = 'accounts/email_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserEmailVerification(View):
    def get(self, request, *args, **kwargs):

        email = kwargs['email']
        key = kwargs['activation_key']
        try:
            user = User.objects.get(username=email)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.email_verified == True:
                if user_profile.activation_key == key:
                    cuttent_date_time = timezone.now()
                    if cuttent_date_time <= user_profile.key_expires:
                        user_profile.is_active = True;
                        user_profile.email_verified = True
                        user_profile.save()
                        return redirect(reverse('login'))
                    else:
                        return redirect(reverse('register'))
                else:
                    return redirect(reverse('register'))
            else:
                messages.success(request, "your email is verified.Login")
                return redirect(reverse('login'))
        except User.DoesNotExist:
            return redirect(reverse('register'))