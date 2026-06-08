from django.contrib import admin

from users.models import Skill, User

admin.site.empty_value_display = "Не задано"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "surname", "phone", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "name", "surname", "phone")
    ordering = ("email",)
    filter_horizontal = ("skills", "groups", "user_permissions")
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields": ("email", "password", "last_login")}),
        (
            "Профиль",
            {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")},
        ),
        ("Навыки", {"fields": ("skills",)}),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
