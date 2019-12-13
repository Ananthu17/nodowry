from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('filter', login_required(QuickFilter.as_view()), name='filter'),
    path('confirm-email', ConfirmYourEmail.as_view(), name='confirm-email'),
    path('profile', login_required(Profile.as_view()), name='profile'),
    path('user-profile', login_required(UserProfileDetails.as_view()), name='user-profile'),
    path('subscribe-mail', SubscribeMail.as_view(), name='subscribe-mail'),
    path('upload-image', UploadImage.as_view(), name='upload-image'),
    path('upload-user-image', UploadUserImage.as_view(), name='upload-user-image'),
    path('delete-image', csrf_exempt(DeleteImage.as_view()), name='delete-image'),
    path('select-cast', csrf_exempt(SelectCast.as_view()), name='select-cast'),
    path('select-sub-cast', csrf_exempt(SelectSubCast.as_view()), name='select-sub-cast'),
    path('select-education', csrf_exempt(SelectEducation.as_view()), name='select-education'),
    path('profile-details', csrf_exempt(SaveProfileDetails.as_view()), name='profile-details'),
    path('partner-details', csrf_exempt(SavePartnerDetails.as_view()), name='partner-details'),
    path('change-user-image', csrf_exempt(ChangeUserImage.as_view()), name='change-user-image'),
    path('update-basic-info', csrf_exempt(UpdateBasicInfo.as_view()), name='update-basic-info'),
    path('update-partner-pref', csrf_exempt(UpdatePartnerPref.as_view()), name='update-partner-pref'),
    path('partner-details-template/<int:profile_id>/', login_required(csrf_exempt(PartnerDetails.as_view())), name='partner-details-template'),
]