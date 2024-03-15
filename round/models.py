from django.db import models
from jdatetime import datetime as jdatetime


class Round(models.Model):
    title = models.CharField('عنوان', blank=True, null=True, max_length=512)
    year = models.IntegerField('سال برگزاری', blank=True, null=True)
    price = models.IntegerField('هزینه', blank=True, null=True)
    round = models.IntegerField('دوره', blank=True, null=True)

    created_at = models.DateTimeField('زمان ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)
    created_ja_at = models.CharField('تاریخ شمسی', max_length=10, default=jdatetime.now().strftime('%Y/%m/%d'))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'