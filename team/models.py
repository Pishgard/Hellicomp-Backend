from django.db import models
from jdatetime import datetime as jdatetime
from phonenumber_field.modelfields import PhoneNumberField

from round.models import Round


class DiscountCode(models.Model):
    title = models.CharField('عنوان کد', blank=True, null=True, max_length=512)
    code = models.CharField('کد تخفیف', blank=True, null=True, max_length=512)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='round_discount_code',
                                 verbose_name='دوره', blank=True, null=True)
    percent = models.IntegerField('درصد تخفیف', blank=True, null=True)
    amount = models.IntegerField('میزان تخفیف', blank=True, null=True)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    created_ja_at = models.CharField('تاریخ شمسی', max_length=10, default=jdatetime.now().strftime('%Y/%m/%d'))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف ها'


class Team(models.Model):

    STATUS_GRADE = (
        ('7', 'هفتم'),
        ('8', 'هشتم'),
        ('9', 'نهم'),
    )

    STATUS_PAYMENT = (
        ('waiting', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('unpaid', 'پرداخت نشده'),
    )

    name = models.CharField('نام تیم', blank=True, null=True, max_length=512)
    school = models.CharField('نام مدرسه', blank=True, null=True, max_length=512)
    city = models.CharField('نام شهر', blank=True, null=True, max_length=512)
    grade = models.CharField('مقطع تحصیلی', max_length=128, choices=STATUS_GRADE, blank=True, null=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='round_team',
                              verbose_name='دوره', blank=True, null=True)

    username = models.CharField('نام کاربری', blank=True, null=True, max_length=512)
    password = models.CharField('رمز عبور', blank=True, null=True, max_length=512)

    first_name_1 = models.CharField('نام شرکت کننده اول', blank=True, null=True, max_length=512)
    last_name_1 = models.CharField('نام خانوادگی شرکت کننده اول', blank=True, null=True, max_length=512)
    national_code_1 = models.CharField('کد ملی شرکت کننده اول', max_length=10, unique=True, null=True, blank=True)
    phone_1 = PhoneNumberField('شماره موبایل شرکت کننده اول', null=True, blank=True)
    parent_phone_1 = PhoneNumberField('شماره موبایل والدین شرکت کننده اول', null=True, blank=True)
    email_1 = models.EmailField('آدرس ایمیل شرکت کننده اول', max_length=255, null=True, blank=True)

    first_name_2 = models.CharField('نام شرکت کننده دوم', blank=True, null=True, max_length=512)
    last_name_2 = models.CharField('نام خانوادگی شرکت کننده دوم', blank=True, null=True, max_length=512)
    national_code_2 = models.CharField('کد ملی شرکت کننده دوم', max_length=10, unique=True, null=True, blank=True)
    phone_2 = PhoneNumberField('شماره موبایل شرکت کننده دوم', null=True, blank=True)
    parent_phone_2 = PhoneNumberField('شماره موبایل والدین شرکت کننده دوم', null=True, blank=True)
    email_2 = models.EmailField('آدرس ایمیل شرکت کننده دوم', max_length=255, null=True, blank=True)

    pyment_status = models.CharField('وضعیت پرداخت',  max_length=128, choices=STATUS_PAYMENT, default='waiting')
    pyment_serial = models.CharField('شماره پیگیری', blank=True, null=True, max_length=512)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='discount_code_team',
                              verbose_name='تخفیف', blank=True, null=True)

    active = models.BooleanField('فعال بودن', default=False)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    created_ja_at = models.CharField('تاریخ شمسی', max_length=10, default=jdatetime.now().strftime('%Y/%m/%d'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم ها'