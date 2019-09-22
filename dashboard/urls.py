from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('users', DashboardUsers.as_view(), name='dashboard-users'),
    path('', DashboardLogIn.as_view(), name='dashboard-login'),
    path('logout', DashboardLogOut.as_view(), name='dashboard-logout'),
    path('edit-user/<int:user_profile_id>/', EditUsert.as_view(), name='edit-user'),
]