from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('filter', QuickFilter.as_view(), name='filter'),
    path('confirm-email', ConfirmYourEmail.as_view(), name='confirm-email'),
    path('profile', Profile.as_view(), name='profile'),
    path('subscribe-mail', SubscribeMail.as_view(), name='subscribe-mail')
]