from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name")}),
    )
