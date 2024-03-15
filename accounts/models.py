from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (AbstractUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from jdatetime import datetime as jdatetime

from team.models import Team


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):

        if username is None:
            raise TypeError("Users should have an Phone")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class UserDetails(models.Model):
    school_name = models.CharField(max_length=128, default=None, null=True, blank=True)
    province = models.CharField(max_length=128, default=None, null=True, blank=True)
    city = models.CharField(max_length=128, default=None, null=True, blank=True)
    address = models.TextField(default=None, null=True, blank=True)
    postal_code = models.CharField(max_length=10, default=None, null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birth_date = models.DateField(default=None, null=True, blank=True)
    father_name = models.CharField(max_length=128, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.school_name}"

    class Meta:
        ordering = ('id',)
        verbose_name = 'جزئیات کاربر'
        verbose_name_plural = 'جزئیات کاربران'


class User(AbstractUser):
    STATUS_GENDER = (
        ('men', 'مذکر'),
        ('women', 'مونث'),
    )

    STATUS_TYPE = (
        ('user', 'کاربر'),
        ('team', 'تیم'),
    )

    email = models.EmailField('آدرس ایمیل', max_length=255, null=True, blank=True)
    email_verified = models.BooleanField('معتبر بودن ایمیل', default=False)
    phone = PhoneNumberField('شماره موبایل', unique=True, null=True, blank=True)
    phone_verified = models.BooleanField('معتبر بودن شماره', null=True, blank=True)
    parent_phone = PhoneNumberField('شماره موبایل', unique=True, null=True, blank=True)
    gender = models.CharField('جنسیت', max_length=128, choices=STATUS_GENDER, default='men')
    type = models.CharField('نوع', max_length=128, choices=STATUS_TYPE, default='user')

    team_detail = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_detail_user',
                               verbose_name='جزئیات تیم', blank=True, null=True)
    user_details = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='user_detailsـuser', default=None,
                                     verbose_name='جزئیات کاربر', null=True, blank=True)

    active = models.BooleanField('فعال بودن', default=False)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    deleted_at = models.DateTimeField('تاریخ حذف', blank=True, null=True)
    created_ja_at = models.CharField('تاریخ شمسی', max_length=10, default=jdatetime.now().strftime('%Y/%m/%d'))

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.get_full_name():
            name = self.get_full_name()
        else:
            name = self.phone.as_national.replace(" ", "-")
        return name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'expire_at': str(timezone.now() + refresh.access_token.lifetime)
        }

    def __str__(self):
        return f"{self.phone}"

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class UserTeam(models.Model):

    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_user_1',
                               verbose_name='عضو اول', blank=True, null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_user_2',
                               verbose_name='عضو دوم', blank=True, null=True)
    user_team = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_user_team',
                                  verbose_name='تیم', blank=True, null=True)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    created_ja_at = models.CharField('تاریخ شمسی', max_length=10, default=jdatetime.now().strftime('%Y/%m/%d'))

    def __str__(self):
        return f"{self.user_team.first_name}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'کاربر تیم'
        verbose_name_plural = 'کاربر تیم ها'


class OTPRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp',
                                 verbose_name='کاربر', blank=True, null=True)
    request_id = models.CharField('آیدی رکوئست', max_length=50, null=True, blank=True)
    otp = models.CharField('کد تایید', max_length=6, null=True, blank=True)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    deleted_at = models.DateTimeField('تاریخ حذف', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('id',)
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کد تایید ها'