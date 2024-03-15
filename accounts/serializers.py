from rest_framework import serializers
from .models import *
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class LoginPhoneSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()
    otp = serializers.CharField(max_length=6)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone', 'otp', 'tokens')

    def get_tokens(self, obj):
        """A method for returning the tokens"""
        user = User.objects.get(phone=obj['phone'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
            'expire_at': user.tokens()['expire_at']
        }

class SendOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class LoginPasswordSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'tokens')

    def get_tokens(self, obj):
        """A method for returning the tokens"""
        user = User.objects.get(phone=obj['phone'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
            'expire_at': user.tokens()['expire_at']
        }

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        password = attrs.get('password', '')

        user = auth.authenticate(phone=phone, password=password)


        if not user:
            raise AuthenticationFailed('Invalid Credentials, try agian!')
        if not user.active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.phone_verified:
            raise AuthenticationFailed('Phone is not verified')
        return {
            'phone': user.phone,
            'tokens': user.tokens()
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class SendOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField()



class PasswordResetSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    otp = serializers.CharField()
    password = serializers.CharField()