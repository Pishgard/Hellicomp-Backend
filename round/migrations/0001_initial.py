# Generated by Django 4.2.11 on 2024-03-15 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=512, null=True, verbose_name='عنوان')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='سال برگزاری')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='هزینه')),
                ('round', models.IntegerField(blank=True, null=True, verbose_name='دوره')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('created_ja_at', models.CharField(default='1402/12/25', max_length=10, verbose_name='تاریخ شمسی')),
            ],
            options={
                'verbose_name': 'دوره',
                'verbose_name_plural': 'دوره ها',
                'ordering': ('-created_at',),
            },
        ),
    ]