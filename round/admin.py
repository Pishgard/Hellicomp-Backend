from django.contrib import admin
from .models import *


@admin.register(Round)
class UrlVisitLogAdmin(admin.ModelAdmin):
    # Define the list of fields to be displayed in the admin page
    list_display = ['title', 'price', 'year', 'created_at', 'updated_at', 'created_ja_at']

    # Define the list of filters to be displayed on the right-hand side
    list_filter = ['title', 'created_at']

    # Define the list of fields that should be read-only in the admin page
    readonly_fields = ['created_at']