from django.contrib import admin
from .models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'address_type', 'is_default', 'created_at']
    list_filter = ['address_type', 'is_default', 'country']
    search_fields = ['user__username', 'full_name', 'city', 'postal_code']
