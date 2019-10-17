from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from dashboard.models import *
from django.urls import reverse
from datetime import date
from django.contrib import messages

class HomePage(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['religion_list'] = Religion.objects.all()
        context['language_list'] = MotherTongue.objects.all()
        return context


class QuickFilter(TemplateView):
    template_name = 'frontend/filterscreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gender = self.request.GET.get('gender')
        agefrom = int(self.request.GET.get('agefrom'))
        ageto = int(self.request.GET.get('ageto'))
        religion_id = self.request.GET.get('religion')
        language = self.request.GET.get('language')
        currentdate = date.today()
        startdate = currentdate.replace(currentdate.year - agefrom)
        enddate = currentdate.replace(currentdate.year - ageto)
        userprofile = UserProfile.objects.filter(is_active=True, gender=gender, userinfo__religion=religion_id, userinfo__mother_tongue=language, userinfo__dob__range=(enddate, startdate)).values('user__first_name', 'userinfo__userimages__file', 'userinfo__dob', 'gender')
        context['user_profile'] = userprofile
        context['user_count'] = userprofile.count()
        context['agefrom'] = agefrom
        context['ageto'] = ageto
        return context


class ConfirmYourEmail(TemplateView):
    template_name = 'frontend/confirm-your-email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Profile(TemplateView):
    template_name = 'frontend/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(id=41)
        context['user_profile'] = user
        context['user_images'] = UserImages.objects.filter(user_info__user_profile=user)
        context['religion_list'] = Religion.objects.all()
        return context


class SubscribeMail(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', "")
        message = "Subscription successful"
        messages.success(request, message)
        return redirect(reverse('home'))


class UploadImage(View):

    def post(self, request, *args, **kwargs):
        user_info_id = request.POST.get('id', "")
        image = request.FILES.get('photos')
        print(user_info_id)
        print(image)
        user_info = UserInfo.objects.get(id=user_info_id)
        user_image = UserImages()
        user_image.user_info = user_info
        user_image.file = image
        user_image.save()
        return redirect(reverse('profile'))


class DeleteImage(View):

    def post(self, request, *args, **kwargs):
        imgid = request.POST.get('imgId', "")
        try:
            UserImages.objects.filter(id=imgid).delete()
            messages.success(request, "image is deleted")
        except UserImages.DoesNotExist:
            messages.error(request, "images not deleted")
        return redirect(reverse('profile'))


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
        print("Cast ")
        print(cast)
        try:
            cast_obj = Cast.objects.get(id=1)
            result = SubCast.objects.filter(religion=cast_obj).values('id','name')
            return JsonResponse({'data': list(result)})
        except Cast.DoesNotExist:
            return redirect(reverse('profile'))


class SelectEducation(View):

    def get(self, request, *args, **kwargs):
        try:
            education = Education.objects.all().values()
            print(education)
            return JsonResponse({'data': list(education)})
        except Education.DoesNotExist:
            return redirect(reverse('profile'))