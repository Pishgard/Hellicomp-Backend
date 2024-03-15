from django.urls import path
from .views import *

app_name = 'team'

urlpatterns = [
    path('', TeamAPIView.as_view(), name='team_create'),
    path('list/', TeamlListView.as_view(), name='team_create'),
]