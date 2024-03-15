from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from .serializers import *
from accounts.models import User, UserDetails, UserTeam
from .models import Team
from round.models import Round

import random
import string


class TeamlListView(generics.ListAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


def generate_random_password(length):
    # ترکیب کلیدهای مورد نظر برای تولید رمز
    characters = string.ascii_letters + string.digits + string.punctuation
    # تولید رمز تصادفی
    random_password = ''.join(random.choice(characters) for i in range(length))
    return random_password


class TeamAPIView(APIView):
    serializer_class = TeamSerializer

    def post(self, request):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(random.choice(characters) for i in range(8))
        data = self.request.data
        name = data['name']
        city = data['city']
        school = data['school']
        round = data['round']

        user_first_name_1 = data['user_first_name_1']
        user_last_name_1 = data['user_last_name_1']
        user_email_1 = data['user_email_1']
        user_phone_1 = data['user_phone_1']
        national_code_1 = data['national_code_1']
        user_parent_phone_1 = data['user_parent_phone_1']

        user_first_name_2 = data['user_first_name_2']
        user_last_name_2 = data['user_last_name_2']
        user_email_2 = data['user_email_2']
        user_phone_2 = data['user_phone_2']
        national_code_2 = data['national_code_2']
        user_parent_phone_2 = data['user_parent_phone_2']

        round_item = Round.objects.get(round=round)

        if Team.objects.exists():
            latest_team = Team.objects.latest('id')
            new_team_id = latest_team.id + 1
        else:
            new_team_id = 1

        team_username = f"t_{round}{100 + new_team_id}"

        if len(national_code_1) != 10 or not national_code_1.isdigit() or UserDetails.objects.filter(national_code=national_code_1).exists():
            raise ValidationError(f"کد ملی {national_code_1} نادرست است")

        if len(national_code_2) != 10 or not national_code_2.isdigit() or UserDetails.objects.filter(national_code=national_code_2).exists():
            raise ValidationError(f"کد ملی {national_code_2} نادرست است")

        team_details = Team.objects.create(
            first_name_1=user_first_name_1,
            last_name_1=user_last_name_1,
            email_1=user_email_1,
            phone_1=user_phone_1,
            national_code_1=national_code_1,
            parent_phone_1=user_parent_phone_1,

            first_name_2=user_first_name_2,
            last_name_2=user_last_name_2,
            email_2=user_email_2,
            phone_2=user_phone_2,
            national_code_2=national_code_2,
            parent_phone_2=user_parent_phone_2,

            username=team_username,
            password=random_password,
            name=name,
            city=city,
            school=school,
            round=round_item
        )

        team_acc = User.objects.create(
            username=team_username,
            password=random_password,
            first_name=name,
            team_detail=team_details,
            type='team'
        )

        if User.objects.exists():
            latest_user = User.objects.latest('id')
            new_user_id = latest_user.id + 1
        else:
            new_user_id = 1

        user_details_1 = UserDetails.objects.create(
            school_name=school,
            city=city,
            national_code=national_code_1,
        )

        random_password = ''.join(random.choice(characters) for i in range(8))

        user_1_username = f"u_{round}{100 + new_user_id}"
        user_1 = User.objects.create(
            username=user_1_username,
            password=random_password,
            first_name=user_first_name_1,
            last_name=user_last_name_1,
            email=user_email_1,
            phone=user_phone_1,
            user_details=user_details_1,
            type='user'
        )

        user_details_2 = UserDetails.objects.create(
            school_name=school,
            city=city,
            national_code=national_code_2,
        )

        random_password = ''.join(random.choice(characters) for i in range(8))

        user_2_username = f"u_{round}{100 + new_user_id + 1}"
        user_2 = User.objects.create(
            username=user_2_username,
            password=random_password,
            first_name=user_first_name_2,
            last_name=user_last_name_2,
            email=user_email_2,
            phone=user_phone_2,
            user_details=user_details_2,
            type='user'
        )

        user_team = UserTeam.objects.create(
            user_1=user_1,
            user_2=user_2,
            user_team=team_acc
        )

        serializer = self.serializer_class(team_details)
        return Response({
            'success': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
