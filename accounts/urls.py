from django.urls import path

from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email/', EmailConfirmation.as_view(), name='email'),
]