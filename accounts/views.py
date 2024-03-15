from tokenize import TokenError
from rest_framework import generics, views, serializers, permissions, status
from .serializers import *
from rest_framework.response import Response
from random import randint, seed
from time import time
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated


class LoginPhoneAPIView(generics.GenericAPIView):
    serializer_class = LoginPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.objects.filter(phone=data["phone"]).exists():
                user = get_object_or_404(User, phone=data["phone"])
            else:
                user = User.objects.create(phone=data['phone'])
            info = get_object_or_404(OTPRequest, user=user)
            if info.otp == data["otp"]:
                user.phone_verified = True
                user.active = True
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'OTP code is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class SendOTPAPIView(generics.GenericAPIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        seed(time())
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.objects.filter(phone=data["phone"]).exists():
                user = get_object_or_404(User, phone=data["phone"])
            else:
                user = User.objects.create(phone=data['phone'])

            verification_code = randint(100000, 999999)
            if OTPRequest.objects.filter(user=user).exists():
                otp = get_object_or_404(OTPRequest, user=user)
                otp.otp = verification_code
                otp.save()
            else:
                import random
                uuid = ''.join( [chr(random.randint(0, 255)) for i in range(0, 15)])
                OTPRequest.objects.create(user=user, otp=verification_code, request_id=uuid)
            return Response({'success': True, 'message': 'Your request Accepted', 'code': verification_code,}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class CustomTokenRefreshview(TokenRefreshView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({"Error": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LoginPasswordAPIView(generics.GenericAPIView):
    """Login View"""
    serializer_class = LoginPasswordSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)

        return Response(serializers.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["پسورد وارد شده اشتباه است."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response({"success": ["پسورد با موفقیت تغییر کرد."]}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPAPIView(generics.GenericAPIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        seed(time())
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            data = serializer.validated_data
            phone = data["phone"]
            if User.objects.filter(phone=data["phone"]).exists():
                user = get_object_or_404(User, phone=data["phone"])

                verification_code = randint(100000, 999999)
                import requests

                url = "https://rest.ippanel.com/v1/messages/patterns/send"
                headers = {
                    "Authorization": "AccessKey 9i3SStpTxsr9IpOVDskU9XjRr8TMFG1vLxVK9qqqzhc=",
                    "Content-Type": "application/json"
                }
                data = {
                    'pattern_code': 'k2i6c2txv7hu0s2',
                    'originator': '+98100020400',
                    "recipient" : f'{phone}',
                    'values' : {
                        'otp': str(verification_code),
                    }
                }

                response = requests.post(url, headers=headers, json=data)
                # print(response.status_code)
                # print(response.text)
            else:
                return Response({'message': 'کاربر یافت نشد' }, status=status.HTTP_404_NOT_FOUND)
            if OTPRequest.objects.filter(user=user).exists():
                otp = get_object_or_404(OTPRequest, user=user)
                otp.otp = verification_code
                otp.save()
            else:
                import random
                uuid = ''.join([chr(random.randint(0, 255)) for i in range(0, 15)])
                OTPRequest.objects.create(user=user, otp=verification_code, request_id=uuid)

            return Response({'success': True, 'message': 'کد با موفقیت ارسال شد'}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        password = serializer.validated_data['password']
        user = get_object_or_404(User, phone=phone)
        if user:
            info = get_object_or_404(OTPRequest, user=user)
            if info.otp == otp:
                time_diff = timezone.now() - info.updated_at
                time_diff_seconds = time_diff.total_seconds()
                time_diff_minutes = time_diff_seconds / 60
                if time_diff_minutes < 3:
                    user.set_password(password)
                    user.save()
                    return Response({'success': True, 'message': 'پسورد جدید با موفقیت ثبت شد'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'کد منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'کد اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'کاربری با این شماره یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)