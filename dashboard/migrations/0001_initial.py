# Generated by Django 2.2.5 on 2019-11-26 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cast_created_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MotherTongue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='religion_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='religion_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Cast')),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcast_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcast_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='-', max_length=10)),
                ('phone_number', models.CharField(max_length=12)),
                ('reset_key', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('reset_key_expiration', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_user', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_fb', models.BooleanField(default=False)),
                ('activation_key', models.CharField(blank=True, max_length=100)),
                ('key_expires', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('email_verified', models.BooleanField(default=False)),
                ('otp_message', models.IntegerField(blank=True, null=True)),
                ('phone_number_verified', models.BooleanField(default=False, null=True)),
                ('first_time_login', models.BooleanField(default=True, null=True)),
                ('profile_pic', models.ImageField(null=True, upload_to='user_images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matrimony_id', models.CharField(blank=True, max_length=10, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('hobies', models.CharField(blank=True, max_length=50, null=True)),
                ('bodytype', models.CharField(blank=True, max_length=50, null=True)),
                ('physical_status', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('dist', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=50, null=True)),
                ('eating', models.CharField(blank=True, max_length=50, null=True)),
                ('drinking', models.CharField(blank=True, max_length=50, null=True)),
                ('smoking', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('salary', models.FloatField(blank=True, max_length=50, null=True)),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('paid_status', models.BooleanField(default=False)),
                ('about', models.TextField(blank=True, max_length=500, null=True)),
                ('gotra', models.CharField(blank=True, max_length=50, null=True)),
                ('star', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_created_for', models.CharField(blank=True, max_length=50, null=True)),
                ('cast', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Cast')),
                ('education', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Education')),
                ('mother_tongue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.MotherTongue')),
                ('religion', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Religion')),
                ('subcast', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.SubCast')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='user_images/')),
                ('is_profile_pic', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(null=True, upload_to='user_images/')),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('expiry', models.DateTimeField(blank=True)),
                ('coast', models.FloatField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bodytype', models.CharField(blank=True, max_length=50, null=True)),
                ('age_from', models.IntegerField(blank=True, null=True)),
                ('age_to', models.IntegerField(blank=True, null=True)),
                ('physical_status', models.CharField(blank=True, max_length=50, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=50, null=True)),
                ('gotra', models.CharField(blank=True, max_length=50, null=True)),
                ('star', models.CharField(blank=True, max_length=50, null=True)),
                ('dosh', models.CharField(blank=True, max_length=50, null=True)),
                ('cast', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Cast')),
                ('religion', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Religion')),
                ('subcast', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.SubCast')),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='cast',
            name='religion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Religion'),
        ),
        migrations.AddField(
            model_name='cast',
            name='updated_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cast_updated_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
