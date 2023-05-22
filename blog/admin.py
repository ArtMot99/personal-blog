from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import User, Category, Post


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "author"]
    list_filter = ["categories"]
    search_fields = ["title"]
