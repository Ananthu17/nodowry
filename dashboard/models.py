import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


def random_number_generator(size=25, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Create your models here.


class UserProfile(models.Model):
    """
    Model for saving extra credentials like phone number, gender etc.
    This model can be inherited to get make appropriate user profile models
    """
    # CHOICE = (
    #     ('-', '-'),
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('others', 'Other'),
    # )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,  default='-')
    phone_number = models.CharField(max_length=12)
    reset_key = models.CharField(max_length=30, blank=True, null=True, default='')
    reset_key_expiration = models.DateTimeField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_fb = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=100, blank=True)
    key_expires = models.DateTimeField(default=timezone.now, blank=True)
    email_verified = models.BooleanField(default=False)
    otp_message = models.IntegerField(blank=True, null=True)
    phone_number_verified = models.BooleanField(default=False, null=True)
    first_time_login = models.BooleanField(default=True, null=True)
    profile_pic = models.ImageField(upload_to='user_images/', null=True)
    customer_id = models.CharField(max_length=200,default="")


    def __str__(self):
        return self.user.username

    def set_reset_key(self):
        self.reset_key = random_number_generator()
        self.reset_key_expiration = timezone.now() + timedelta(hours=1)

    def verify_reset_key_expiry(self):
        if timezone.now() <= self.reset_key_expiration:
            return True
        else:
            return False


class MotherTongue(models.Model):
    """
       Model for saving all the mother tongue uploaded by the admin.

    """
    language = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.language


class Education(models.Model):
    """
       Model for saving all the education related uploaded by the admin.

    """
    field = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.field


class Religion(models.Model):
    """
        Model for saving all the religion names  uploaded by the admin.

   """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,  related_name='religion_created_user')
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,  related_name='religion_updated_user')

    def __str__(self):
        return self.name


class Cast(models.Model):
    """
        Model for saving all the cast names  uploaded by the admin.

    """
    name = models.CharField(max_length=50)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,  related_name='cast_created_user')
    updated_by = models.ForeignKey(User, blank=True,  on_delete=models.CASCADE,  related_name='cast_updated_user')

    def __str__(self):
        return self.name


class SubCast(models.Model):
    """
        Model for saving all the subcast names  uploaded by the admin.

    """
    name = models.CharField(max_length=50)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,  related_name='subcast_created_user')
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,  related_name='subcast_updated_user')

    def __str__(self):
        return self.name


class Plans(models.Model):
    """
        Model is used for saving the plans created by admin
        admin can select plans as foreign key
    """
    name = models.CharField(max_length=30)
    expiry = models.DateTimeField(blank=True,null=True)
    amount = models.FloatField(null=True, blank=True, default=None)
    plan_id = models.CharField(null=True, blank=True,max_length=40)
    period = models.CharField(default="monthly",null=True,max_length=40)
    interval = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='plans_created_user')
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='plans_updated_user')
    archived = models.BooleanField(default=False)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    Model for saving all the details of a user.
    This model can be inherited to get make appropriate user profile models
    """
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    matrimony_id = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    mother_tongue = models.ForeignKey(MotherTongue, blank=True, on_delete=models.CASCADE, null=True)
    education = models.ForeignKey(Education, blank=True, on_delete=models.CASCADE, null=True)
    religion = models.ForeignKey(Religion, blank=True, on_delete=models.CASCADE, default="", null=True)
    cast = models.ForeignKey(Cast, blank=True, on_delete=models.CASCADE, default="", null=True)
    subcast = models.ForeignKey(SubCast, blank=True, on_delete=models.CASCADE, default="", null=True)
    hobies = models.CharField(max_length=50, blank=True, null=True)
    bodytype = models.CharField(max_length=50, blank=True, null=True)
    physical_status = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    dist = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    eating = models.CharField(max_length=50, null=True, blank=True)
    drinking = models.CharField(max_length=50, null=True, blank=True)
    smoking = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    salary = models.FloatField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    paid_status = models.BooleanField(default=False)
    about = models.TextField(max_length=500, null=True, blank=True)
    gotra = models.CharField(max_length=50, null=True, blank=True)
    star = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    profile_created_for = models.CharField(max_length=50, null=True, blank=True)
    subscribed_plan = models.ForeignKey(Plans,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.user_profile.user.email

    def age(self):
        return int((datetime.now().date() - self.dob).days / 365.25)


class UserImages(models.Model):
    """
   Model for saving all the images uploaded by the user.

   """
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='user_images/')
    is_profile_pic = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to='user_images/', null=True)

    def __str__(self):
        return self.user_info.user_profile.user.email




class PartnerPreference(models.Model):
    """
   Model for saving all the images uploaded by the user.

   """
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    bodytype = models.CharField(max_length=50, blank=True, null=True)
    age_from = models.IntegerField( blank=True, null=True)
    age_to = models.IntegerField( blank=True, null=True)
    physical_status = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    religion = models.ForeignKey(Religion, blank=True, on_delete=models.CASCADE, default="", null=True)
    cast = models.ForeignKey(Cast, blank=True, on_delete=models.CASCADE, default="", null=True)
    subcast = models.ForeignKey(SubCast, blank=True, on_delete=models.CASCADE, default="", null=True)
    gotra = models.CharField(max_length=50, null=True, blank=True)
    star = models.CharField(max_length=50, null=True, blank=True)
    dosh = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user_info.user_profile.user.email


class PlanSubscriptionList(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=30,null=True,blank=True)
    payment_date = models.DateField(auto_now_add=True)
    subscribed_plan = models.ForeignKey(Plans,on_delete=models.CASCADE)
    amount_charged = models.CharField(max_length=20,null=True)
    subscription_id = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=20,default="created")
    payment_url = models.CharField(max_length=30,default="")

    def __str__(self):
        return self.user.user.email


class Testimonials(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Awards(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
