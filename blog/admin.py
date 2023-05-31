from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import User, Category, Post, Comment, ContactMessage


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "post", "created_at", "author"]
    search_fields = ["text"]
    list_filter = ["created_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "email", "created_at"]
    list_filter = ["created_at"]
