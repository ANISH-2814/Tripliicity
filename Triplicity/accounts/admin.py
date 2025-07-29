from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerificationOTP


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_email_verified', 'is_staff', 'created_at')
    list_filter = ('is_email_verified', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extended Profile', {
            'fields': ('phone', 'address', 'city', 'state', 'country', 'postal_code', 'date_of_birth', 'profile_picture')
        }),
        ('Email Verification', {
            'fields': ('is_email_verified', 'email_verification_token')
        }),
        ('Preferences', {
            'fields': ('preferred_destinations', 'travel_interests', 'budget_range')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EmailVerificationOTP)
class EmailVerificationOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'otp_code')
    readonly_fields = ('created_at',)
