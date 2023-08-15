from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_chief_commune', 'is_nationalAdministrator', 'last_login', 'image',)
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_chief_commune', 'is_nationalAdministrator', 'is_superuser', 'is_active')
    fieldsets = (
        ('User Credential', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender', 'commune', 'phone', ('profilePicture',),)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_chief_commune', 'is_nationalAdministrator', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('New User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'gender', 'gender', 'commune', 'phone', ('profilePicture',),),
        }),
        ('Permission', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_chief_commune', 'is_nationalAdministrator', 'user_permissions',),
        }),
        ('User Credential', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    ordering = ('email',)
    list_editable = ()
    list_per_page = 10
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.unregister(Group)
