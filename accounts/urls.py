from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('token/refresh/', CustomTokenRefreshview.as_view(), name='token_refresh'),
    path('otp/', SendOTPAPIView.as_view(), name='otp'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('login-password/', LoginPasswordAPIView.as_view(), name='login'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]