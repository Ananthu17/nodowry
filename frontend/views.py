from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from dashboard.models import *
from django.urls import reverse
from datetime import date
from django.contrib import messages
from dashboard.elasticsearch import *


class HomePage(TemplateView):
    template_name = 'frontend/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['religion_list'] = Religion.objects.all()
        context['language_list'] = MotherTongue.objects.all()
        if self.request.user.is_authenticated:
            user_obj = self.request.user
            try:
                user = UserProfile.objects.get(user=user_obj)
            except:
                messages.error(self.request,"User profile does not exist")
                logout(self.request)
            context['user_profile'] = user
            context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        context['religion_list'] = Religion.objects.all()
        context['mother_tongue'] = MotherTongue.objects.all()
        context['awards_list'] = Awards.objects.all()
        context['testimonial_list'] = Testimonials.objects.all()
        return context


class QuickFilter(TemplateView):
    template_name = 'frontend/filterscreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gender = self.request.GET.get('gender','')
        agefrom = int(self.request.GET.get('agefrom',18))
        ageto = int(self.request.GET.get('ageto',35))
        religion_id = self.request.GET.get('religion','')
        cast_id = self.request.GET.get('cast','')
        language = self.request.GET.get('language','')
        currentdate = date.today()
        startdate = currentdate.replace(currentdate.year - agefrom)
        enddate = currentdate.replace(currentdate.year - ageto)
        userprofile = UserProfile.objects.filter(is_active=True, gender=gender, userinfo__religion=religion_id,
                                                 userinfo__mother_tongue=language,
                                                 userinfo__dob__range=(enddate, startdate)).values('user__first_name',
                                                                                                   'userinfo__dob',
                                                                                                   'gender',
                                                                                                   'profile_pic',
                                                                                                   'userinfo__city',
                                                                                                   'userinfo__state',
                                                                                                   'userinfo__dist',
                                                                                                   'userinfo__mother_tongue',
                                                                                                   'userinfo__cast__name',
                                                                                                   'userinfo__education__field',
                                                                                                   'id','userinfo__height')
        context['user_profile'] = userprofile
        context['user_count'] = userprofile.count()
        context['agefrom'] = agefrom
        context['ageto'] = ageto
        context['religion_list'] = Religion.objects.all()
        context['cast_list'] = Cast.objects.all()
        context['language_list'] = MotherTongue.objects.all()
        religion_name = Religion.objects.get(id = religion_id)

        context['relid'] = religion_name.name
        context['language'] = language
        context['gender'] = gender

        if self.request.user.is_authenticated:
            context['user_images'] = UserImages.objects.filter(user_info__user_profile__user=self.request.user)
        return context


class ConfirmYourEmail(TemplateView):
    template_name = 'frontend/confirm-your-email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Profile(TemplateView):
    template_name = 'frontend/profile.html'

    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request,*args,**kwargs)
        try:
            user_obj = self.request.user
            user = UserProfile.objects.get(user=user_obj)
        except:
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        user = UserProfile.objects.get(user=user_obj)
        context['user_profile'] = user
        context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        context['religion_list'] = Religion.objects.all()
        context['mother_tongue'] = MotherTongue.objects.all()
        return context


class SubscribeMail(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', "")
        if email == "":
            message = "Email field empty"
        else:
            message = "Subscription successful"
        messages.success(request, message)
        return redirect(reverse('home'))


class UploadImage(View):
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request,*args,**kwargs)
        referer = request.META.get('HTTP_REFERER')
        try:
            user_info_id = request.POST.get('id', "")
            try:
                image = request.FILES.get('photos')

            except:
                messages.error(request,"Images required")
                return redirect(referer)
        except:
            messages.error(request, "Invalid User info")
            return redirect(referer)
        return context

    def post(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        user_info_id = request.POST.get('id', "")
        if user_info_id != "":
            try:
                image = request.FILES.get('photos')
            except:
                messages.error(request, "Images required")
                return redirect(referer)
            try:
                user_info = UserInfo.objects.get(id=user_info_id)
                user_image = UserImages()
                user_image.user_info = user_info
                user_image.file = image
                user_image.save()
            except:
                messages.error(request, "User does not exist")
                return redirect(referer)
        else:
            messages.error(request, "User id cannot be empty")
            return redirect(referer)


        return redirect(reverse('home'))


class DeleteImage(View):

    def post(self, request, *args, **kwargs):
        imgid = request.POST.get('imgId', "")
        try:
            UserImages.objects.filter(id=imgid).delete()
            messages.success(request, "image is deleted")
        except UserImages.DoesNotExist:
            messages.error(request, "images not deleted")
        return redirect(reverse('home'))


class SelectCast(View):

    def post(self, request, *args, **kwargs):
        religion = request.POST.get('religion', "")
        print(religion)
        try:
            religion_obj = Religion.objects.get(name=religion)
            cast = Cast.objects.filter(religion=religion_obj).values('id', 'name')
            return JsonResponse({'data': list(cast)})
        except Religion.DoesNotExist:
            return redirect(reverse('profile'))


class SelectSubCast(View):

    def post(self, request, *args, **kwargs):
        cast = request.POST.get('cast', "")
        try:
            cast_obj = Cast.objects.get(name=cast)
            result = SubCast.objects.filter(cast=cast_obj).values('id', 'name')
            print(result)
            return JsonResponse({'data': list(result)})
        except Cast.DoesNotExist:
            return redirect(reverse('profile'))


class SelectEducation(View):

    def get(self, request, *args, **kwargs):
        try:
            education = Education.objects.all().values()
            return JsonResponse({'data': list(education)})
        except Education.DoesNotExist:
            return redirect(reverse('profile'))


class SaveProfileDetails(View):


    def post(self, request, *args, **kwargs):

        user_id = int(request.POST.get('id', ""))
        address = request.POST.get('address', "")
        state = request.POST.get('state', "")
        dist = request.POST.get('dist', "")
        city = request.POST.get('city', "")
        religion = request.POST.get('religion', "")
        cast = request.POST.get('cast', "")
        subcast = request.POST.get('subcast', "")
        gotra = request.POST.get('gotra', "")
        star = request.POST.get('star', "")
        bodyType = request.POST.get('body-type', "")
        drinking = request.POST.get('drinking', "")
        smoking = request.POST.get('smoking', "")
        education = request.POST.get('education', "")
        profession = request.POST.get('profession', "")
        marital = request.POST.get('marital', "")
        physical = request.POST.get('physical', "")
        height = float(request.POST.get('height', ""))
        weight = float(request.POST.get('weight', ""))
        eating = request.POST.get('eating', "")
        about = request.POST.get('about', "")
        try:
            user_info = UserInfo.objects.get(id=user_id)
            user_info.state = state
            user_info.dist = dist
            user_info.address = address
            user_info.city = city
            user_info.religion = Religion.objects.get(name=religion)
            user_info.cast = Cast.objects.get(name=cast)
            user_info.subcast = SubCast.objects.get(name=subcast)
            user_info.education = Education.objects.get(field=education)
            user_info.drinking = drinking
            user_info.smoking = smoking
            user_info.profession = profession
            user_info.marital_status = marital
            user_info.physical_status = physical
            user_info.bodytype = bodyType
            user_info.height = height
            user_info.weight = weight
            user_info.gotra = gotra
            user_info.star = star
            user_info.eating = eating
            user_info.about = about
            user_info.save()
            message = "Item Successfully Added"

            return JsonResponse({'data': message})
        except UserInfo.DoesNotExist:
            message = "Item is not added"
        return JsonResponse({'data': message})


class SavePartnerDetails(View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_id = request.POST.get('id', "")
        bodyType = request.POST.get('bodyType', "")
        ageFrom = request.POST.get('ageFrom', "")
        ageTo = request.POST.get('ageTo', "")
        physicalstatus = request.POST.get('physicalstatus', "")
        maritalstatus = request.POST.get('maritalstatus', "")
        religion = request.POST.get('religion', "")
        cast = request.POST.get('cast', "")
        subcast = request.POST.get('subcast', "")
        gotram = request.POST.get('gotram', "")
        star = request.POST.get('star', "")
        dosh = request.POST.get('dosh', "")
        try:
            user_info = UserInfo.objects.get(id=user_id)
            partner_pref = PartnerPreference()
            partner_pref.user_info = user_info
            partner_pref.bodytype = bodyType
            partner_pref.age_from = ageFrom
            partner_pref.age_to = ageTo
            partner_pref.physical_status = physicalstatus
            partner_pref.marital_status = maritalstatus
            partner_pref.religion = Religion.objects.get(name=religion)
            partner_pref.cast = Cast.objects.get(name=cast)
            partner_pref.subcast = SubCast.objects.get(name=subcast)
            partner_pref.gotra = gotram
            partner_pref.star = star
            partner_pref.dosh = dosh
            partner_pref.save()
            message = "Item Successfully Added"
            user_profile = UserProfile.objects.get(user=user)
            user_profile.first_time_login = False
            user_profile.save()
        except UserInfo.DoesNotExist:
            message = "Item is not added"
        return JsonResponse({'data': message})


class UserProfileDetails(TemplateView):
    template_name = 'frontend/user-profile.html'
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request,*args,**kwargs)
        referer = request.META.get('HTTP_REFERER')
        user_obj = self.request.user
        try:
            user = UserProfile.objects.get(user=user_obj)
            user_info_obj = UserInfo.objects.get(user_profile=user)
            context['partner_pref'] = PartnerPreference.objects.get(user_info=user_info_obj)
        except:
            messages.error(request,"User could not be found")
            return redirect(referer)

        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        user = UserProfile.objects.get(user=user_obj)
        context['user_profile'] = user
        user_info_obj = UserInfo.objects.get(user_profile=user)
        context['partner_pref'] = PartnerPreference.objects.get(user_info=user_info_obj)
        context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        context['mother_tongue'] = MotherTongue.objects.all()
        context['religion_list'] = Religion.objects.all()
        context['matches'] = Matches.objects.filter(matched_partner=user)
        return context


class DisplayImages(View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        userimages = UserImages.objects.filter(user_info__user_profile__user=user)
        # userimages = UserImages.objects.filter(user_info__user_profile__user__email="timsavage@yopmail.com")
        JsonResponse({'data': userimages})


class PartnerDetails(TemplateView):
    template_name = 'frontend/partner-details.html'
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request,*args,**kwargs)
        referer = request.META.get('HTTP_REFERER')
        try:
            profile_id = kwargs['profile_id']
            user_obj = self.request.user
            user = UserProfile.objects.get(user=user_obj)
            user_info_obj = UserInfo.objects.get(user_profile=user)


            context['partner_pref'] = PartnerPreference.objects.get(user_info=user_info_obj)
            partner_profile = UserProfile.objects.get(id=profile_id)
            partner_info = UserInfo.objects.get(user_profile=partner_profile)

            gender = str(partner_profile.gender)
            mother_tongue = str(partner_info.mother_tongue.language)
            religion = str(partner_info.religion.name)
            cast = str(partner_info.cast.name)
            subcast = str(partner_info.subcast.name)
            dob = partner_info.dob
            similar_results = els_lan.query_data(gender, mother_tongue, religion, cast, subcast)
            context['similar_results'] = similar_results

        except:
            messages.error(request, "User could not be found")
            return redirect(referer)

        return context
    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated:
        profile_id = kwargs['profile_id']
        context = super().get_context_data(**kwargs)

        user_obj = self.request.user
        user = UserProfile.objects.get(user=user_obj)
        context['user_profile'] = user
        user_info_obj = UserInfo.objects.get(user_profile=user)
        context['partner_pref'] = PartnerPreference.objects.get(user_info=user_info_obj)
        context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        partner_profile = UserProfile.objects.get(id=profile_id)
        partner_info = UserInfo.objects.get(user_profile=partner_profile)
        partner_images = UserImages.objects.filter(user_info=partner_info)
        context['parter_profile'] = partner_profile
        context['parter_info'] = partner_info
        context['partner_images'] = partner_images
        gender = str(partner_profile.gender)
        mother_tongue = str(partner_info.mother_tongue.language)
        religion = str(partner_info.religion.name)
        cast = str(partner_info.cast.name)
        subcast = str(partner_info.subcast.name)
        dob = partner_info.dob
        similar_results = els_lan.query_data(gender, mother_tongue, religion, cast, subcast)
        context['similar_results'] = similar_results
        # else:
        #     pass
        return context


class ChangeUserImage(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('imgupload', "")
        print(image)
        user_obj = self.request.user
        userprofile = UserProfile.objects.get(user=user_obj)
        userprofile.profile_pic = image
        userprofile.save()
        return redirect(reverse('user-profile'))


class UpdateBasicInfo(View):
    def post(self, request, *args, **kwargs):
        profile_id = int(request.POST.get('profile_id', ""))
        referer = request.META.get('HTTP_REFERER')
        name = request.POST.get('name', "")
        gender = request.POST.get('gender', "")
        mother_tongue = request.POST.get('mother_tongue', "")
        physical_status = request.POST.get('physical_status', "")
        marital_status = request.POST.get('marital_status', "")
        height = request.POST.get('Height', "")
        weight = request.POST.get('Weight', "")
        eating = request.POST.get('eating', "")
        drinking = request.POST.get('drinking', "")
        smoking = request.POST.get('smoking', "")
        try:
            userprofile = UserProfile.objects.get(id=profile_id)
            userprofile.gender = gender
            userprofile.save()
            user = User.objects.get(id = userprofile.user.id)
            user.first_name = name
            user.save()
            user_info = UserInfo.objects.get(user_profile=userprofile)
            user_info.mother_tongue = MotherTongue.objects.get(language= mother_tongue)
            user_info.physical_status = physical_status
            user_info.marital_status = marital_status
            user_info.height= height
            user_info.weight = weight
            user_info.eating = eating
            user_info.drinking = drinking
            user_info.smoking = smoking
            user_info.save()
        except:
            messages.error(request,"User profile not found")
        return redirect(reverse('user-profile'))


class UpdatePartnerPref(View):
    def post(self, request, *args, **kwargs):
        profile_id = int(request.POST.get('profile_id', ""))
        agefrom = request.POST.get('ageFrom', "")
        ageto = request.POST.get('ageTo', "")
        mother_tongue_partner = request.POST.get('mother_tongue_partner', "")
        religion_partner = request.POST.get('religion-dropdown-partner', "")
        cast_partner = request.POST.get('cast-dropdown-partner', "")
        subcast_partner = request.POST.get('subcast-dropdown-partner', "")
        gotra_partner = request.POST.get('gotra-partner', "")
        star_patner = request.POST.get('star-patner', "")
        dosh_partner = request.POST.get('dosh-partner', "")
        physical_partner = request.POST.get('physical-partner', "")
        try:
            userprofile = UserProfile.objects.get(id=profile_id)
            user_info = UserInfo.objects.get(user_profile=userprofile)
            partner_pref = PartnerPreference.objects.get(user_info=user_info)
            partner_pref.age_from = agefrom
            partner_pref.age_to = ageto
            partner_pref.religion = Religion.objects.get(name=religion_partner)
            partner_pref.cast = Cast.objects.get(name=cast_partner)
            partner_pref.subcast = SubCast.objects.get(name=subcast_partner)
            partner_pref.gotra = gotra_partner
            partner_pref.star = star_patner
            partner_pref.dosh = dosh_partner
            partner_pref.physical_status = physical_partner
            partner_pref.save()
        except:
            messages.error(request, "User profile not found")
        return redirect(reverse('user-profile'))


class UploadUserImage(View):

    def post(self, request, *args, **kwargs):
        user_info_id = request.POST.get('id', "")
        image = request.FILES.get('photos')
        print(user_info_id)
        print(image)
        try:
            user_info = UserInfo.objects.get(id=user_info_id)
            user_image = UserImages()
            user_image.user_info = user_info
            user_image.file = image
            user_image.save()
        except:
            messages.error(request, "User profile not found")
        return redirect(reverse('user-profile'))


class TestimonialInfo(View):

    def get(self, request, *args, **kwargs):
        test_id = request.GET['test_id']
        try:
            item = Testimonials.objects.get(id=test_id)
            JsonResponse({'data': item})
        except Awards.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class ShowInterest(View):

    def get(self, request, *args, **kwargs):
        profile_id = kwargs['profile_id']
        partner_id = kwargs['partner_id']
        match = Matches()
        match.matched_user = UserProfile.objects.get(id=profile_id)
        match.matched_partner = UserProfile.objects.get(id=partner_id)
        match.save()
        return redirect('partner-details-template', partner_id)

