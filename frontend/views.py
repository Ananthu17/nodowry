import json

import requests
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from dashboard.models import *
from django.urls import reverse
from datetime import date
from django.contrib import messages
import razorpay
import logging

razorpay_client = razorpay.Client(auth=("rzp_test_pLn7iGkMQ3dorZ", "UrETBkY9UtXnpyXVvFZZTBQO"))
from dashboard.elasticsearch import *
from django.core.mail import send_mail
from django.template import loader
import razorpay

logger = logging.getLogger(__name__)
razorpay_client = razorpay.Client(auth=("rzp_test_pLn7iGkMQ3dorZ", "UrETBkY9UtXnpyXVvFZZTBQO"))


def send_payment_email(context):
    email = context['email']
    template = loader.get_template("frontend/subscription-start.html")
    email_content = template.render(context)
    send_mail(
        'No Dowry Marriage - Subscription',
        email_content,
        'help@nodowry.com',
        [email],
        html_message=email_content,
        fail_silently=False
    )


def send_matching_email(context):
    email = context['email']
    template = loader.get_template("accounts/interest_notification.html")
    email_content = template.render(context)
    send_mail(
        'NoDowry Person Matching',
        email_content,
        'help@nodowry.com',
        [email],
        html_message=email_content,
        fail_silently=False
    )


class HomePage(TemplateView):
    template_name = 'frontend/index.html'

    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request, *args, **kwargs)
        if request.user.is_superuser or request.user.is_staff:
            return redirect(reverse('dashboard'))
        else:
            return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['religion_list'] = Religion.objects.all()
        context['language_list'] = MotherTongue.objects.all()
        context['religion_list'] = Religion.objects.all()
        context['mother_tongue'] = MotherTongue.objects.all()
        context['awards_list'] = Awards.objects.all()

        context['testimonial_list'] = Testimonials.objects.all()
        if self.request.user.is_superuser:
            return redirect(reverse('dashboard'))
        else:
            if self.request.user.is_authenticated:
                user_obj = self.request.user
                user = UserProfile.objects.get(user=user_obj)
                try:

                    try:
                        user_info = UserInfo.objects.get(user_profile__user=self.request.user)
                    except:
                        user.first_time_login = True
                        user.save()
                except:

                    messages.error(self.request, "User profile does not exist")
                    logout(self.request)
                context['user_profile'] = user
                context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
            return context


class QuickFilter(TemplateView):
    template_name = 'frontend/filterscreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gender = self.request.GET.get('gender', '')
        agefrom = int(self.request.GET.get('agefrom', 18))
        ageto = int(self.request.GET.get('ageto', 35))
        religion_id = self.request.GET.get('religion', '')
        cast_id = self.request.GET.get('cast', '')
        language = self.request.GET.get('language', '')
        height_min = self.request.GET.get('height_min', 50)
        height_max = self.request.GET.get('height_max', 220)
        currentdate = date.today()
        startdate = currentdate.replace(currentdate.year - agefrom)
        enddate = currentdate.replace(currentdate.year - ageto)
        userprofile = UserProfile.objects.filter(is_active=True, gender=gender, userinfo__religion=religion_id,
                                                 userinfo__mother_tongue=language,
                                                 userinfo__dob__range=(enddate, startdate), userinfo__height__lte=height_max, userinfo__height__gte=height_min).values('user__first_name',
                                                                                                   'userinfo__dob',
                                                                                                   'gender',
                                                                                                   'profile_pic',
                                                                                                   'userinfo__city',
                                                                                                   'userinfo__state',
                                                                                                   'userinfo__dist',
                                                                                                   'userinfo__mother_tongue',
                                                                                                   'userinfo__cast__name',
                                                                                                   'userinfo__education__field',
                                                                                                   'id',
                                                                                                   'userinfo__height')
        context['user_profile'] = userprofile
        context['user_count'] = userprofile.count()
        context['agefrom'] = agefrom
        context['ageto'] = ageto
        context['religion_list'] = Religion.objects.all()
        context['cast_list'] = Cast.objects.all()
        context['language_list'] = MotherTongue.objects.all()

        religion_name = Religion.objects.get(id=religion_id)
        language_name = MotherTongue.objects.get(id=language)

        context['relid'] = religion_name.name
        context['language_name'] = language_name
        context['gender'] = gender

        context['height_min'] = height_min
        context['height_max'] = height_max

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
        context = super().dispatch(request, *args, **kwargs)
        try:
            user_obj = self.request.user
            user = UserProfile.objects.get(user=user_obj)
            return context
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
        context = super().dispatch(request, *args, **kwargs)
        referer = request.META.get('HTTP_REFERER')
        try:
            user_info_id = request.POST.get('id', "")
            try:
                image = request.FILES.get('photos')

            except:
                messages.error(request, "Images required")
                return redirect(referer)
        except:
            messages.error(request, "Invalid User info")
            return redirect(referer)
        return context

    def post(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        user_info_id = request.POST.get('id', "")
        user_obj = self.request.user
        user_profile_obj = UserProfile.objects.get(user=user_obj)
        # if not user_profile_obj.profile_pic:
        #     empty_profile_pic = True

        if user_info_id != "":
            try:
                user_info = UserInfo.objects.get(id=user_info_id)
            except:
                messages.error(request, "User does not exist")
                return redirect(referer)

            try:
                for idx, file in enumerate(request.FILES.getlist('photos')):

                    if idx == 0 and not user_profile_obj.profile_pic:
                        print("############################################################")
                        print(file)
                        user_profile_obj.profile_pic = file
                        user_profile_obj.save()
                    else:
                        user_image = UserImages()
                        user_image.user_info = user_info
                        user_image.file = file
                        user_image.save()

                profile_pic = UserProfile.objects.filter(id = user_profile_obj.id).values('profile_pic')
                profile_images = UserImages.objects.filter(user_info=user_info).values('file', 'id')

                # if not user_profile_obj.profile_pic:
                #     print("############################################################")
                #     print(profile_pic)
                #     UserProfile.objects.filter(user=user_obj).update(profile_pic=profile_pic)
                #     print("############################################################")
                #     print("Updated")
            except:
                messages.error(request, "Images required")
                return redirect(referer)

        else:
            messages.error(request, "User id cannot be empty")
            return redirect(referer)

        return JsonResponse({'profile_pic': list(profile_pic), 'profile_images': list(profile_images)})


class DeleteImage(View):

    def post(self, request, *args, **kwargs):
        imgid = request.POST.get('imgId', "")
        try:
            UserImages.objects.filter(id=imgid).delete()
            profile_images = UserImages.objects.filter(user_info__user_profile__user=request.user).values('file', 'id')
        except UserImages.DoesNotExist:
            pass
        return JsonResponse({'profile_images': list(profile_images)})


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
        user_obj = request.user

        user_id = request.POST.get('id', "")
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
            # user_info.subcast = SubCast.objects.get(name=subcast)
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
        gotram = request.POST.get('gotram', "")
        star = request.POST.get('star', "")
        dosh = request.POST.get('dosh', "")
        if religion:
            religion_obj = Religion.objects.get(name=religion)
        else:
            religion_obj = None

        if cast:
            cast_obj = Cast.objects.get(name=cast)
        else:
            cast_obj = None

        try:
            user_info = UserInfo.objects.get(id=user_id)
            partner_pref_obj, created = PartnerPreference.objects.update_or_create(user_info=user_info,
                                                                                   defaults={'user_info': user_info})

            partner_pref_obj.bodyType = bodyType
            partner_pref_obj.age_from = ageFrom
            partner_pref_obj.age_to = ageTo
            partner_pref_obj.physical_status = physicalstatus
            partner_pref_obj.marital_status = maritalstatus
            partner_pref_obj.gotra = gotram
            partner_pref_obj.star = star
            partner_pref_obj.dosh = dosh
            partner_pref_obj.religion = religion_obj
            partner_pref_obj.cast = cast_obj
            partner_pref_obj.save()

            # partner_pref = PartnerPreference()
            # partner_pref.user_info = user_info
            # partner_pref.bodytype = bodyType
            # partner_pref.age_from = ageFrom
            # partner_pref.age_to = ageTo
            # partner_pref.physical_status = physicalstatus
            # partner_pref.marital_status = maritalstatus
            # partner_pref.religion = Religion.objects.get(name=religion)
            # partner_pref.cast = Cast.objects.get(name=cast)
            # partner_pref.subcast = SubCast.objects.get(name=subcast)
            # partner_pref.gotra = gotram
            # partner_pref.star = star
            # partner_pref.dosh = dosh
            # partner_pref.save()

            message = "Item Successfully Added"
            user_profile = UserProfile.objects.get(user=user)
            user_profile.first_time_login = False
            user_profile.save()

            raw_data = list(UserProfile.objects.filter(id=user_profile.id).values('user__first_name',
                                                                                  'gender',
                                                                                  'userinfo__religion__name',
                                                                                  'profile_pic',
                                                                                  'userinfo__city',
                                                                                  'userinfo__state',
                                                                                  'userinfo__dist',
                                                                                  'userinfo__mother_tongue__language',
                                                                                  'userinfo__cast__name',
                                                                                  'id', 'userinfo__height',
                                                                                  'is_active',
                                                                                  'userinfo__religion__name',
                                                                                  'userinfo__dob',
                                                                                  'userinfo__occupation',

                                                                                  ))
            els_lan.updatedata(raw_data)
        except UserInfo.DoesNotExist:
            message = "Item is not added"
        return JsonResponse({'data': message})


class UserProfileDetails(TemplateView):
    template_name = 'frontend/user-profile.html'

    def dispatch(self, request, *args, **kwargs):

        context = super().dispatch(request, *args, **kwargs)
        referer = request.META.get('HTTP_REFERER')
        user_obj = self.request.user
        try:

            user = UserProfile.objects.get(user=user_obj)
            user_info_obj = UserInfo.objects.get(user_profile=user)
            context['partner_pref'] = PartnerPreference.objects.filter(user_info=user_info_obj)
        except:
            messages.error(request, "User could not be found")
            return redirect(referer)

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        user = UserProfile.objects.get(user=user_obj)

        context['user_profile'] = user
        # try:
        user_info_obj = UserInfo.objects.get(user_profile__user=user_obj)

        context['partner_pref'] = PartnerPreference.objects.filter(user_info=user_info_obj)[0]
        # except :
        #     pass
        context['plans'] = Plans.objects.filter(archived=False)
        context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        context['mother_tongue'] = MotherTongue.objects.all()
        context['religion_list'] = Religion.objects.all()
        context['subs'] = ""
        try:
            subscribed_plans = PlanSubscriptionList.objects.get(user=user_info_obj.user_profile)
            subscription_id =subscribed_plans.subscription_id
            headers = {
                'Content-Type': 'application/json',
            }
            data = {
                "cancel_at_cycle_end": 1
            }
            url = "https://api.razorpay.com/v1/subscriptions/" + subscription_id + ""
            r = requests.get(url, headers=headers, data=json.dumps(data),
                              auth=('rzp_test_pLn7iGkMQ3dorZ', 'UrETBkY9UtXnpyXVvFZZTBQO'))
            serv_response = r.json()
            context['subs'] = serv_response

        except:
            pass

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

        context = super().dispatch(request, *args, **kwargs)
        referer = request.META.get('HTTP_REFERER')
        try:
            profile_id = kwargs['profile_id']
            user_obj = self.request.user
            user = UserProfile.objects.get(user=user_obj)
            try:
                user_info_obj = UserInfo.objects.get(user_profile=user)
                context['partner_pref'] = PartnerPreference.objects.get(user_info=user_info_obj)
                partner_profile = UserProfile.objects.get(id=profile_id)
                partner_info = UserInfo.objects.get(user_profile=partner_profile)
                gender = str(partner_profile.gender)

                if partner_info.mother_tongue:
                    mother_tongue = str(partner_info.mother_tongue.language)
                else:
                    mother_tongue = ""

                religion = ""
                cast = ""
                subcast = ""
                try:
                    religion = str(partner_info.religion.name)
                    cast = str(partner_info.cast.name)
                    subcast = str(partner_info.subcast.name)

                except:
                    pass
                dob = partner_info.dob
                similar_results = els_lan.query_data(gender, mother_tongue, religion, cast, subcast)
                context['similar_results'] = similar_results
            except Exception as e:

                messages.error(request, str(e))
                return redirect('/')



        except UserInfo.DoesNotExist:
            messages.error(request, "User could not be found")
            return redirect('/')

        except:
            messages.error(request, "User could not be found")
            return redirect(referer)

        return context

    def get_context_data(self, **kwargs):

        print('Something went wrong!')
        try:
            # if self.request.user.is_authenticated:
            profile_id = kwargs['profile_id']
            context = super().get_context_data(**kwargs)

            user_obj = self.request.user
            user = UserProfile.objects.get(user=user_obj)
            context['user_profile'] = user
            user_info_obj = UserInfo.objects.get(user_profile=user)
            context['partner_pref'] = PartnerPreference.objects.filter(user_info=user_info_obj)[0]
            context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
            partner_profile = UserProfile.objects.get(id=profile_id)
            partner_info = UserInfo.objects.get(user_profile=partner_profile)
            partner_images = UserImages.objects.filter(user_info=partner_info)
            matches_list = Matches.objects.filter(matched_partner=partner_profile, matched_user=user)
            print("################################################### 528")
            print(matches_list)
            context['parter_profile'] = partner_profile
            context['parter_info'] = partner_info
            context['partner_images'] = partner_images
            context['matches_list'] = matches_list
            mother_tongue = str(partner_info.mother_tongue.language)
            gender = str(partner_profile.gender)

            religion = ""
            cast = ""
            subcast = ""
            dob = ""
            try:
                religion = str(partner_info.religion.name)
                cast = str(partner_info.cast.name)
                subcast = str(partner_info.subcast.name)
                dob = partner_info.dob
            except:
                pass

            similar_results = els_lan.query_data(gender, mother_tongue, religion, cast, subcast)
            context['similar_results'] = similar_results
            # else:
            #     pass
        except:
            pass
        return context

    def post(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        ndm_full_id = request.POST.get('ndmid', "")


        print(ndm_full_id)
        print("#############################################################")
        ndm_id = ndm_full_id[4:]
        try:
            partner_profile = UserProfile.objects.get(id=ndm_id)
            partner_info = UserInfo.objects.get(user_profile=partner_profile)
            print(ndm_id)
            return redirect('partner-details-template', profile_id=ndm_id)
        except:
            messages.error(request,'NDM id mismatch')
            return redirect(referer)


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
            user = User.objects.get(id=userprofile.user.id)
            user.first_name = name
            user.save()
            user_info = UserInfo.objects.get(user_profile=userprofile)
            user_info.mother_tongue = MotherTongue.objects.get(language=mother_tongue)
            user_info.physical_status = physical_status
            user_info.marital_status = marital_status
            user_info.height = height
            user_info.weight = weight
            user_info.eating = eating
            user_info.drinking = drinking
            user_info.smoking = smoking
            user_info.save()
        except:
            messages.error(request, "User profile not found")
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
            partner_pref = PartnerPreference.objects.filter(user_info=user_info)[0]
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
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
            partner_profile = UserProfile.objects.get(id=partner_id)
            try:
                Matches.objects.get(matched_partner=partner_profile, matched_user=user_profile).delete()
                print(str(profile_id) + " ----> " + str(partner_id))
                print("#########################################################################")
                print("It has been deleted")
            except Matches.DoesNotExist:
                print(str(profile_id) + " ----> " + str(partner_id))
                print("#########################################################################")
                print("Creating an interest")
                Matches.objects.create(matched_user=user_profile, matched_partner=partner_profile)
                ''' creating the mail confirmation url  '''
                context = {}
                context['partner_name'] = partner_profile.user.first_name
                context['user_name'] = user_profile.user.first_name
                context['email'] = partner_profile.user.email
                context['matching_profile_url'] = request.scheme + "://" + request.META["HTTP_HOST"] + reverse(
                    'partner-details-template', kwargs={'profile_id': profile_id})
                '''
                sending verification mail to the user
                '''
                send_matching_email(context)

        except UserProfile.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect('partner-details-template', partner_id)


def quick_search_limited(request):
    gender = request.GET.get('gender', '')
    start_age = int(request.GET.get('start_age', 18))
    final_age = int(request.GET.get('final_age', 35))
    religion = request.GET.get('religion', '')
    mother_tongue = request.GET.get('mother_tongue', '')
    print(gender)
    print(start_age)
    print(final_age)
    print(religion)
    print(mother_tongue)

    current_date = date.today()

    startdate = current_date.replace(current_date.year - start_age)
    enddate = current_date.replace(current_date.year - final_age)
    userprofiles = UserProfile.objects.filter(is_active=True, gender=gender, userinfo__religion=religion,
                                              userinfo__mother_tongue=mother_tongue,
                                              userinfo__dob__range=(enddate, startdate)).values('user__first_name',
                                                                                                'gender',
                                                                                                'profile_pic',
                                                                                                'userinfo__religion__name',
                                                                                                'userinfo__subcast__name',
                                                                                                'userinfo__cast__name',
                                                                                                'userinfo__city',
                                                                                                'userinfo__state',
                                                                                                'userinfo__dist',
                                                                                                'userinfo__mother_tongue',
                                                                                                'userinfo__cast__name',
                                                                                                'userinfo__education__field',
                                                                                                'userinfo__profession',
                                                                                                'userinfo__height')[:6]
    dict = []
    for users in userprofiles:
        dict.append(users)

    return JsonResponse({'data': dict})


class SubscribePlan(View):
    def get(self, request, *args, **kwargs):
        plan_id = kwargs['plan_id']
        user_obj = request.user
        subscribe_url = "https://api.razorpay.com/v1/subscriptions"
        headers = {
            'Content-Type': 'application/json',
        }

        if plan_id != '':
            try:
                plan_obj = Plans.objects.get(id=plan_id)
                user_profile = UserProfile.objects.get(user=user_obj)
                user_info = UserInfo.objects.get(user_profile=user_profile)
                try:
                    plns = PlanSubscriptionList.objects.get(user=user_profile)
                    plns.delete()
                except:
                    pass
                if user_profile.customer_id != '':
                    payload_data = {
                        "plan_id": plan_obj.plan_id,
                        "total_count": 1,
                        "quantity": 1,
                        "customer_notify": 1,
                        "addons": [],
                        "notes": {
                            "notes_key": "Started Subscription"
                        },
                        "notify_info": {
                            "notify_phone": user_profile.phone_number,
                            "notify_email": user_obj.username
                        }
                    }
                else:

                    create_customer_payload = {
                        "name": user_profile.user.first_name,
                        "email": user_profile.user.email,
                        "contact": user_profile.phone_number,
                        "notes": {},
                        "fail_existing": 0
                    }
                    create_customer = razorpay_client.customer.create(data=create_customer_payload)
                    customer_id = create_customer['id']
                    user_profile.customer_id = customer_id
                    user_profile.save()
                    payload_data = {
                        "plan_id": plan_obj.plan_id,
                        "total_count": 1,
                        "quantity": 1,
                        "customer_notify": 1,
                        "addons": [],
                        "notes": {
                            "notes_key": "Started Subscription"
                        },
                        "notify_info": {
                            "notify_phone": user_profile.phone_number,
                            "notify_email": user_obj.username
                        }
                    }
                # subscribe_data = razorpay_client.subscription.create(data=payload_data)
                payload_data = json.dumps(payload_data)
                r = requests.post('https://api.razorpay.com/v1/subscriptions', headers=headers, data=payload_data,
                                  auth=('rzp_test_pLn7iGkMQ3dorZ', 'UrETBkY9UtXnpyXVvFZZTBQO'))
                subscribe_data = r.json()
                subscription_id = subscribe_data['id']
                short_url = subscribe_data['short_url']
                plan_sub_obj = PlanSubscriptionList.objects.create(user=user_profile, subscription_id=subscription_id,
                                                                   subscribed_plan=plan_obj, payment_url=short_url)
                user_info.subscribed_plan = plan_obj

                user_info.save()
                context = {}
                context['payment_link'] = short_url
                context['plan_name'] = plan_obj.name
                context['amount'] = plan_obj.amount
                context['email'] = user_obj.username
                '''
                sending verification mail to the user
                '''
                send_payment_email(context)

                messages.success(request,
                                 "Subscribed successfully. Link to initiate your first payment has been send to your registered mail id. Please pay the amount to start your subscription")
            except Plans.DoesNotExist:
                messages.error(request, "Plans could not be found")
            except UserProfile.DoesNotExist:
                messages.error(request, "Userprofile does not exist")
            except UserInfo.DoesNotExist:
                messages.error(request, "Userinfo does not exist")
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please choose a valid plan")
        return redirect('/')


def SubscribeWebhook(request):
    if request.method == "POST":
        webhook_body = request
        print(webhook_body)
        return 0
    else:
        return 1


class CancelSubscription(View):
    def get(self, request):
        user_obj = request.user
        try:
            user_profile_obj = UserProfile.objects.get(user=user_obj)
            plans_obj = PlanSubscriptionList.objects.get(user=user_profile_obj)
            user_info_obj = UserInfo.objects.get(user_profile=user_profile_obj)
            subscription_id = plans_obj.subscription_id
            headers = {
                'Content-Type': 'application/json',
            }
            data = {
                "cancel_at_cycle_end": 1
            }
            url = "https://api.razorpay.com/v1/subscriptions/" + subscription_id + "/cancel"
            r = requests.post(url, headers=headers, data=json.dumps(data),
                              auth=('rzp_test_pLn7iGkMQ3dorZ', 'UrETBkY9UtXnpyXVvFZZTBQO'))
            serv_response = r.json()
            try:
                if serv_response['status'] == "cancelled":
                    plans_obj.delete()
                    user_info_obj.subscribed_plan = None
                    user_info_obj.save()

                else:
                    messages.error(request, "Failed to cancel the subscription. Contact admin to rectify")
            except Exception as e:

                messages.success(request, "Subscription could not be cancelled")
                return redirect(reverse("user-profile"))
            messages.success(request, "Subscription Cancelled")

        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found")
        except PlanSubscriptionList.DoesNotExist:
            messages.error(request, "Plan not found")

        return redirect(reverse("user-profile"))
