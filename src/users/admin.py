from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    add_form = UserCreationForm

    ordering = ["email"]
    search_fields = ("email", "last_name", "first_name")
    list_display = ("email", "last_name", "first_name")

    fieldsets = [
        ("Идентификация", {"fields": ["email", "password"]}),
        ("Личная информация", {"fields": ["last_name", "first_name"]}),
        (
            "Права доступа",
            {"fields": ["is_active", "groups", "is_staff", "is_superuser"]},
        ),
    ]
