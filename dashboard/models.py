from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class UserProfile(models.Model):
    """
    Model for saving extra credentials like phone number, gender etc.
    This model can be inherited to get make appropriate user profile models
    """
    CHOICE = (
        ('-', '-'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=CHOICE, default='-')
    phone_number = models.CharField(max_length=12)
    reset_key = models.CharField(max_length=30, blank=True, null=True, default='')
    reset_key_expiration = models.DateTimeField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_fb = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


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
    religion = models.ForeignKey(Cast, on_delete=models.CASCADE)
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
    expiry = models.DateTimeField(blank=True)
    coast = models.FloatField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='plans_created_user')
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='plans_updated_user')

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    Model for saving all the details of a user.
    This model can be inherited to get make appropriate user profile models
    """
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    matrimony_id = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateTimeField(blank=True)
    mother_tongue = models.ForeignKey(MotherTongue, blank=True, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, blank=True, on_delete=models.CASCADE)
    hobies = models.CharField(max_length=50, blank=True)
    bodytype = models.CharField(max_length=50, blank=True)
    physical_status = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
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
    about = models.TextField(max_length=500,null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
