from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "owner__email", "owner__name", "owner__surname")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("name", "description", "status")}),
        ("Ссылки", {"fields": ("github_url",)}),
        ("Участники", {"fields": ("owner", "participants", "created_at")}),
    )
