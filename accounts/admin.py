from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile, SellerProfile


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False

class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (CustomerProfileInline, SellerProfileInline)
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'balance')

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)