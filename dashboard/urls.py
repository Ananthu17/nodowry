from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('users', DashboardUsers.as_view(), name='dashboard-users'),
    path('', DashboardLogIn.as_view(), name='dashboard-login'),
    path('logout', DashboardLogOut.as_view(), name='dashboard-logout'),
    path('edit-user/<int:user_profile_id>/', EditUsert.as_view(), name='edit-user'),
    path('dashboard-content', ContentManagement.as_view(), name='dashboard-content'),
    path('edit-testimonials', EditTestimonials.as_view(), name='edit-testimonials'),
    path('delete-testimonials/<int:test_id>/', EditTestimonials.as_view(), name='delete-testimonials'),
    path('dashboard-filters', FilterContants.as_view(), name='dashboard-filters'),
    path('add-religion', AddReligion.as_view(), name='add-religion'),
    path('add-cast', AddCast.as_view(), name='add-cast'),
    path('add-sub-cast', AddSubCast.as_view(), name='add-sub-cast'),
    path('add-mother-tongue', AddMotherTongue.as_view(), name='add-mother-tongue'),
    path('edit-cast', EditCast.as_view(), name='edit-cast'),
    path('edit-sub-cast', EditSubCast.as_view(), name='edit-sub-cast'),
    path('edit-mother-tongue', EditMotherTongue.as_view(), name='edit-mother-tongue'),
    path('delete-religion/<int:rel_id>/', DeleteReligion.as_view(), name='delete-religion'),
    path('delete-mother-tongue/<int:lang_id>/', DeleteMotherTongue.as_view(), name='delete-mother-tongue'),
    path('delete-cast/<int:cast_id>/', DeleteCast.as_view(), name='delete-cast'),
    path('delete-sub-cast/<int:subCast_id>/', DeleteSubCast.as_view(), name='delete-sub-cast'),
    path('edit-religion', EditReligion.as_view(), name='edit-religion'),
    path('add-award', AwardContant.as_view(), name='add-award'),
    path('delete-award/<int:award_id>/', AwardContant.as_view(), name='delete-award'),
    path('plans-list/', PlansManagement.as_view(), name='dashboard-plans'),
    path('delete-plan/<int:plan_id>/', ManagePlans.as_view(), name='plans-archive'),
    path('subscription-list/', PaymentsList.as_view(), name='subs-list'),
]