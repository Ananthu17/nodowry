from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email/', EmailConfirmation.as_view(), name='email'),
    path('password/', ResetPasswordTemplate.as_view(), name='password'),
    path('forgot-password/', ResetPassword.as_view(), name='forgot-password'),
    path('social-login', SocialLogin.as_view(), name='social_login'),
    re_path(r'email-verification/(?P<activation_key>[\w-]+)/(?P<email>[\w.@+-]+)/', UserEmailVerification.as_view(), name='user-email-verification'),
    re_path(r'user-password-reset-email/(?P<reset_key>[\w-]+)/(?P<email>[\w.@+-]+)/', UserPsswordReset.as_view(), name='user-password-reset'),

]