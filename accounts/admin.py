from django.contrib import admin
from .models import UserDetails, UserTeam, User

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.


# change admin header
admin.site.site_header = "پنل مدیریت حلی کامپ"

# custom user admin


@admin.register(User)
class Useradmin(admin.ModelAdmin):
    list_display = ['username',]
    list_filter = ['created_at',]
    readonly_fields = ['created_at']


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'created_ja_at']
    list_filter = ['created_at',]
    readonly_fields = ['created_at']


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'school_name', 'national_code']
    search_fields = ['id']
