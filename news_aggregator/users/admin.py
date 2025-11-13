from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from news.admin import custom_admin_site
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ['profile_picture']}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додаткова інформація', {'fields': ('email', 'profile_picture')}),
    )


custom_admin_site.register(CustomUser, CustomUserAdmin)
