from rest_framework import serializers
from rest_framework.fields import FileField
from rest_framework.serializers import Serializer

from accounts.serializers import UserSerializer
from .models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

#
#
# class UrlUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Url
#         fields = ('name', 'slug', 'url')
#
#
# class UrlRedirectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Url
#         fields = ('slug',)
#
#
# class UrlCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Url
#         fields = ('name', 'url', 'slug', 'category')
#
#
# class UrlVisitLogSerializer(serializers.ModelSerializer):
#     url = UrlListSerializer()
#
#     class Meta:
#         model = UrlVisitLog
#         fields = '__all__'
#
#
# class UrlCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UrlCategory
#         fields = '__all__'