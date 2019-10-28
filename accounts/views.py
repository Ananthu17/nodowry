from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.models import UserProfile, MotherTongue, Religion, UserInfo, UserImages
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
import urllib.request
import requests
from social_django.models import UserSocialAuth
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


def send_resetpassword_email(context):
    email = context['email']
    template = loader.get_template("accounts/reset_password.html")
    email_content = template.render(context)
    send_mail(
        'NoDowry password reset',
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
        context['mother_tongue'] = MotherTongue.objects.all()
        context['religions'] = Religion.objects.all()
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

            messagetext = str(code) + " Is the OTP for NoDowry Martimony.NEVER SHARE YOUR OTP WITH ANYONE"

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
                    if not UserProfile.objects.filter(phone_number = phone_number):
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
                            message = "A verification mail has been send to registered mail id, Please confirm your mail Id "
                            gender = request.POST.get('gender', "")
                            phone_number = request.POST.get('mobno', "")
                            dob = request.POST.get('dob', "")
                            print("date of birth")
                            date_of_birth = datetime.datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
                            print(dob)
                            print(date_of_birth)
                            language_id = int(request.POST.get('language', ""))
                            religion_id = int(request.POST.get('religion', ""))
                            language = MotherTongue.objects.get(id=language_id)
                            religion = Religion.objects.get(id=religion_id)
                            profilepic = request.FILES.get('uploadFromPC')
                            print(profilepic)
                            userprofile_obj = UserProfile(
                                                    user=user,
                                                    gender=gender,
                                                    phone_number=phone_number,
                                                    phone_number_verified=False,
                                                    is_user=True,
                                                    is_active=False,
                                                    activation_key=activation_key,
                                                    key_expires=activation_key_expiry,
                                                    # otp_message=code
                                                    )
                            userprofile_obj.save()
                            user_info_obj = UserInfo(
                                            user_profile=userprofile_obj,
                                            dob=date_of_birth,
                                            mother_tongue=language,
                                            religion=religion
                            )
                            user_info_obj.save()
                            user_image_obj = UserImages(user_info=user_info_obj, file=profilepic, is_profile_pic=True)
                            user_image_obj.save()
                            messages.success(request, message)
                            return redirect('login')
                        except User.DoesNotExist:
                            messages.error(request, "Something went wrong")
                            return redirect('register')
                    else:
                        messages.error(request, "Phone number is already exist")
                        return redirect('login')
                else:
                    messages.error(request, "user is already exist")
                    return redirect('login')
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
        phone_number = request.POST.get('mobno', '')
        if username != "" and password != "" and phone_number != "":
            try:
                user = User.objects.get(username=username)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if not user.is_superuser:
                        if user_profile.email_verified:
                            if user_profile.phone_number == phone_number:
                            # if user_profile.phone_number_verified:
                                if user_profile.is_active:
                                    if user.check_password(password):
                                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                                        message = "Welcome " + user.first_name
                                        if user_profile.first_time_login:
                                            user_profile.first_time_login = False
                                            user_profile.save()
                                            return redirect(reverse('profile'))
                                        else:
                                            messages.info(request, message)
                                            return redirect(reverse('home'))
                                    else:
                                        messages.error(request, "Invalid Credentials")
                                        return redirect(reverse('login'))
                                else:
                                    messages.error(request, "profile is blocked, Please contact admin")
                                    return redirect(reverse('login'))
                            else:
                                messages.warning(request, "Invalid Phone number")
                                return redirect(reverse('login'))
                            # else:
                            #     messages.warning(request, "Please enter your otp")
                            #     return redirect(reverse('otp-verification'))
                        else:
                            messages.error(request, "Email is not verified.")
                            return redirect(reverse('login'))
                    else:
                        messages.error("Invalid Credentials")
                except UserProfile.DoesNotExist:
                    message = "Something went wrong"
                    messages.error(request, message)
                    return redirect(reverse('login'))
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials, Please try again")
                return redirect(reverse('login'))
        else:
            messages.error(request, "Credentials are not valid")
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


class ResetPasswordTemplate(TemplateView):
    template_name = 'accounts/reset_password.html'

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
            if not user_profile.email_verified:
                if user_profile.activation_key == key:
                    cuttent_date_time = timezone.now()
                    if cuttent_date_time <= user_profile.key_expires:
                        user_profile.is_active = True
                        user_profile.email_verified = True
                        user_profile.save()
                        messages.success(request, "your email is verified please login")
                        return redirect(reverse('login'))
                    else:
                        return redirect(reverse('register'))
                else:
                    return redirect(reverse('register'))
            else:
                messages.success(request, "your email is already verified please login")
                return redirect(reverse('login'))
        except User.DoesNotExist:
            return redirect(reverse('register'))


class ResetPassword(TemplateView):
    template_name = 'accounts/forgot-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', "")
        if email:
            try:
                user = User.objects.get(username=email)
                name = user.first_name
                user_profile = UserProfile.objects.get(user=user)
                user_profile.set_reset_key()
                user_profile.save()
                messages.success(request, "We will email you shortly with instruction on how to reset your password")

                # reset_password_emai(email, reset_password_url_construct(request, user_profile.reset_key)))
                context = {}
                context['email'] = email
                context['name'] = name
                context['url'] = request.scheme + "://" + request.META["HTTP_HOST"] + reverse('user-password-reset', kwargs={'email': email, 'reset_key': user_profile.reset_key})
                send_resetpassword_email(context)
                return redirect(reverse('login'))

            except User.DoesNotExist:
                messages.error(request, "please register")
                return redirect(reverse('login'))
        else:
            messages.error(request, "enter a valid email")
            return redirect(reverse('login'))


class UserPsswordReset(TemplateView):
    template_name = "accounts/change_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        reset_key = kwargs["reset_key"]
        email = kwargs['email']

        if password and confirm_password not in [""]:
            if password == confirm_password:
                user_profile = UserProfile.objects.get(reset_key=kwargs["reset_key"])
                user_profile.user.set_password(password)
                user_profile.user.save(update_fields=["password"])

                user_profile.reset_key = None
                user_profile.reset_key_expiration = None
                user_profile.save()
                messages.success(request, "Your password has been changed. Please try logging in.")
                return redirect(reverse('login'))

            else:
                messages.error(request, "Sorry, password don't match. Please try again")
                return redirect(reverse('user-password-reset', kwargs={'email': email, 'reset_key': reset_key}))
        else:
            messages.error(request, "Please provide valid password")
        return redirect(reverse('login'))


# class ForgotPassword(TemplateView):
#     template_name = 'accounts/forgot-password.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class SocialLogin(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        try:
            user_profile = UserProfile.objects.get(user=user)
            return redirect(reverse('home'))
        except UserProfile.DoesNotExist:
            social_user = UserSocialAuth.objects.get(user=user)
            if social_user.provider == "facebook":
                user_token = social_user.access_token
                url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + user_token
                r = requests.get(url)
                userprofile_obj = UserProfile(
                                        user=user,
                                        is_user=True,
                                        is_active=True,
                                        email_verified=True)
                userprofile_obj.save()
                user_info_obj = UserInfo(user_profile=userprofile_obj)
                user_info_obj.save()
                if r.json()['picture']:
                    user_image_obj = UserImages(user_info=user_info_obj, file=r.json()['picture'], is_profile_pic=True)
                    user_image_obj.save()
                return redirect(reverse('home'))
            else:
                userprofile_obj = UserProfile(
                            user=user,
                            is_user=True,
                            is_active=True,
                            email_verified=True)
                userprofile_obj.save()
                user_info_obj = UserInfo(user_profile=userprofile_obj)
                user_info_obj.save()
                return redirect(reverse('home'))


class OTPVerification(TemplateView):
    template_name = 'accounts/otp-verification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        otp = request.POST.get('otp', "")
        if otp is not None:
            try:
                userprofile = UserProfile.objects.get(otp_message=otp)
                userprofile.phone_number_verified = True
                userprofile.save()
                return redirect(reverse('home'))
            except UserProfile.DoesNotExist:
                messages.error(request, "enter a valid otp")
                return redirect(reverse('otp-verification'))
        else:
            messages.error(request, "enter a valid otp")
            return redirect(reverse('otp-verification'))





