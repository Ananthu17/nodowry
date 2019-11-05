from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import View, TemplateView
from datetime import datetime
from .models import *
import copy
from django.contrib.auth.decorators import user_passes_test


class CheckIsSuperUser:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "Please login for accessing the dashboard")
            return redirect(reverse('dashboard-login'))


class DashboardLogIn(TemplateView):
    template_name = 'dashboard/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        """
        :param request:
        :username:Username
        :password:Password
        """
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username != "" and password != "":
            try:
                user = User.objects.get(username=username)
                if user.is_superuser:
                    if user.is_active:
                        if user.check_password(password):
                            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                            return redirect(reverse('dashboard'))
                        else:
                            messages.error(request, "Invalid Credentials")
                            return redirect(reverse('dashboard-login'))
                    else:
                        messages.error(request, "profile is not active, Please contact admin")
                        return redirect(reverse('dashboard-login'))
                else:
                    messages.error("Invalid Credentials")
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials, Please try again")
                return redirect(reverse('dashboard-login'))
        else:
            messages.error(request, "Username and password is not valid")
            return redirect(reverse('dashboard-login'))


class DashboardLogOut(LoginRequiredMixin, View):
    """
    View for logging out user and redirect to login page
    """
    def get(self, request):
        user = copy.deepcopy(request.user)
        if request.user.is_authenticated:
            logout(request)
            messages.error(request, "You have been logged out. Hope you will be back soon.")
        return redirect(reverse('dashboard-login'))


class Dashboard(LoginRequiredMixin, CheckIsSuperUser, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, *args, **kwargs):

        first_date = self.request.GET.get("start_date", "")
        last_date = self.request.GET.get("end_date", "")
        context = super().get_context_data(**kwargs)
        user_count = UserProfile.objects.all().count()
        deactivated_user_count = UserProfile.objects.filter(is_active=False).count()
        new_users = 0
        if first_date and last_date:
            new_users = UserProfile.objects.filter(created_at__range=(first_date, last_date)).count()
        else:
            end_date = datetime.today()
            start_date = datetime(end_date.year, end_date.month, 1)
            new_users = UserProfile.objects.filter(created_at__range=(start_date, end_date)).count()

        context['user_count'] = user_count
        context['deactivated_user_count'] = deactivated_user_count
        context['new_users'] = new_users
        return context


class DashboardUsers(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = UserProfile.objects.all()
        context['user_list'] = user_list
        return context


class EditUsert(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile_id = kwargs['user_profile_id']
        user_details = UserProfile.objects.get(id=user_profile_id)
        context['user_list'] = user_details
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phonenumber', '')
        user = User.objects.get(username=email)
        user_profile = UserProfile.objects.get(user=user)
        user.first_name = name
        user.email = email
        user.save()
        user_profile.phone_number= phone_number
        user_profile.save()
        return redirect(reverse('dashboard-users'))


class ContentManagement(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        religion = Religion.objects.all()
        cast = Cast.objects.all()
        subcast = SubCast.objects.all()
        mother_tongue = MotherTongue.objects.all()
        context['religion_list'] = religion
        context['cast_list'] = cast
        context['subcast_list'] = subcast
        context['mother_tongue_list'] = mother_tongue
        return context


class AddReligion(LoginRequiredMixin, View):

    def post(self, request, *args, **kwars):
        rel = request.POST.get('lang', '')
        if rel is not None:
            if not Religion.objects.filter(name=rel):
                username = request.user
                religion = Religion()
                religion.name = rel
                religion.created_by = username
                religion.updated_by = username
                religion.save()
            else:
                messages.error(request, "language is already exist")
        return redirect(reverse('dashboard-content'))


class AddCast(LoginRequiredMixin, View):

    def post(self, request, *args, **kwars):
        rel_id = int(request.POST.get('religion', ''))
        cast_name = request.POST.get('cast', '')
        if cast_name is not None:
            if not Cast.objects.filter(name=cast_name):
                username = request.user
                cast = Cast()
                cast.name = cast_name
                cast.religion = Religion.objects.get(id=rel_id)
                cast.created_by = username
                cast.updated_by = username
                cast.save()
            else:
                messages.error(request, "cast already exist")
        return redirect(reverse('dashboard-content'))


class DeleteReligion(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        langid = kwargs['rel_id']
        try:
            Religion.objects.get(id=langid).delete()
            messages.success(request, "Religion Deleted")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class DeleteCast(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cast_id = kwargs['cast_id']
        try:
            Cast.objects.get(id=cast_id).delete()
            messages.success(request, "Religion Deleted")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class EditReligion(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        relid = request.POST.get('relid', '')
        relname = request.POST.get('relName', '')
        username = request.user
        try:
            religion = Religion.objects.get(id=relid)
            religion.name = relname
            religion.updated_by = username
            religion.save()
            print("save successful")
            messages.error(request, "Religion updated successfully")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class EditCast (LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        relid = request.POST.get('religion', '')
        castid = request.POST.get('castid', '')
        castname = request.POST.get('castName', '')
        username = request.user
        try:
            cast = Cast.objects.get(id=castid)
            cast.name = castname
            cast.religion = Religion.objects.get(id=relid)
            cast.updated_by = username
            cast.save()
            print("save successful")
            messages.error(request, "Religion updated successfully")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class AddSubCast(LoginRequiredMixin , View):

    def post(self, request, *args, **kwars):
        cast_id = int(request.POST.get('cast', ''))
        sub_cast_name = request.POST.get('sub-cast', '')
        if sub_cast_name is not None:
            if not SubCast.objects.filter(name=sub_cast_name):
                username = request.user
                subcast = SubCast()
                subcast.name = sub_cast_name
                subcast.cast = Cast.objects.get(id=cast_id)
                subcast.created_by = username
                subcast.updated_by = username
                subcast.save()
            else:
                messages.error(request, "Sub cast is already exist")
        return redirect(reverse('dashboard-content'))


class EditSubCast (LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        castid = request.POST.get('cast', '')
        subcastid = request.POST.get('subCastId', '')
        subcastname = request.POST.get('subCastName', '')
        username = request.user
        try:
            subcast = SubCast.objects.get(id=subcastid)
            subcast.name = subcastname
            subcast.cast = Cast.objects.get(id=castid)
            subcast.updated_by = username
            subcast.save()
            messages.error(request, "Sub Cast updated successfully")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class DeleteSubCast(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        sub_cast_id = kwargs['subCast_id']
        try:
            SubCast.objects.get(id=sub_cast_id).delete()
            messages.success(request, "Item Deleted")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class AddMotherTongue(LoginRequiredMixin, View):

    def post(self, request, *args, **kwars):
        language = request.POST.get('lang', '')
        if language is not None:
            if not MotherTongue.objects.filter(language=language):
                username = request.user
                lang = MotherTongue()
                lang.language = language
                lang.created_by = username
                lang.save()
            else:
                messages.error(request, "language is already exist")
        return redirect(reverse('dashboard-content'))


class EditMotherTongue(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        langid = request.POST.get('langid', '')
        langname = request.POST.get('langName', '')
        try:
            lang = MotherTongue.objects.get(id=langid)
            lang.language = langname
            lang.save()
            messages.error(request, "Religion updated successfully")
        except MotherTongue.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))


class DeleteMotherTongue(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        langid = kwargs['lang_id']
        try:
            MotherTongue.objects.get(id=langid).delete()
            messages.success(request, "Language Deleted")
        except Religion.DoesNotExist:
            messages.error(request, "Something went wrong")
        return redirect(reverse('dashboard-content'))