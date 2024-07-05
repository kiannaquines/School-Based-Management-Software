from django.contrib import admin
from authentication.models import User
from django.contrib.auth.admin import UserAdmin as OriginalAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(OriginalAdmin):

    add_fieldsets = ((None, 
        {
            'fields': ('username','first_name','middle_name','last_name','password1', 'password2', 'email','user_role'),
        },
    ),)

    list_display = ("username","first_name","last_name","email","is_active","is_superuser","user_role","user_gender",)
    search_fields = ("first_name","last_name","username",)
    list_editable = ("is_active","is_superuser","user_role","user_gender",)
    ordering = ("id",)
    list_per_page = 9

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'middle_name','user_profile')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User,CustomUserAdmin)