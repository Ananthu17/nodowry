from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('filter', QuickFilter.as_view(), name='filter'),
    path('confirm-email', ConfirmYourEmail.as_view(), name='confirm-email'),
    path('profile', Profile.as_view(), name='profile'),
    path('user-profile', UserProfileDetails.as_view(), name='user-profile'),
    path('subscribe-mail', SubscribeMail.as_view(), name='subscribe-mail'),
    path('upload-image', UploadImage.as_view(), name='upload-image'),
    path('delete-image', csrf_exempt(DeleteImage.as_view()), name='delete-image'),
    path('select-cast', csrf_exempt(SelectCast.as_view()), name='select-cast'),
    path('select-sub-cast', csrf_exempt(SelectSubCast.as_view()), name='select-sub-cast'),
    path('select-education', csrf_exempt(SelectEducation.as_view()), name='select-education'),
    path('profile-details', csrf_exempt(SaveProfileDetails.as_view()), name='profile-details'),
    path('partner-details', csrf_exempt(SavePartnerDetails.as_view()), name='partner-details'),
    path('partner-details-template/<int:profile_id>/', csrf_exempt(PartnerDetails.as_view()), name='partner-details-template'),
]