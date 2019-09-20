from django.urls import path

from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('users', DashboardUsers.as_view(), name='dashboard-users'),
    path('login', DashboardLogIn.as_view(), name='dashboard-login'),
    path('logout', DashboardLogOut.as_view(), name='dashboard-logout')
]