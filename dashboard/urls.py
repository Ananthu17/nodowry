from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('users', DashboardUsers.as_view(), name='dashboard-users'),
    path('', DashboardLogIn.as_view(), name='dashboard-login'),
    path('logout', DashboardLogOut.as_view(), name='dashboard-logout'),
    path('edit-user/<int:user_profile_id>/', EditUsert.as_view(), name='edit-user'),
    path('dashboard-content', ContentManagement.as_view(), name='dashboard-content'),
    path('add-religion', AddReligion.as_view(), name='add-religion'),
    path('add-cast', AddCast.as_view(), name='add-cast'),
    path('delete-religion/<int:rel_id>/', DeleteReligion.as_view(), name='delete-religion'),
    path('delete-cast/<int:cast_id>/', DeleteCast.as_view(), name='delete-cast'),
    path('edit-religion', EditReligion.as_view(), name='edit-religion'),
]