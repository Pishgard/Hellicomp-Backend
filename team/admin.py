from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

@admin.register(Team)
class TeamAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'created_ja_at']
    list_filter = ['name', 'created_at', 'school']
    readonly_fields = ['created_at']


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'created_at', 'updated_at', 'created_ja_at']
    list_filter = ['title', 'created_at']
    readonly_fields = ['created_at']