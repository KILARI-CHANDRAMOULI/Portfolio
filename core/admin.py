from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Achievement,
    CodingProfile,
    ContactMessage,
    Education,
    Experience,
    ExperienceBullet,
    Language,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tagline", "email", "available_for_work", "is_active")
    list_editable = ("is_active", "available_for_work")
    fieldsets = (
        ("Identity", {"fields": ("full_name", "tagline", "typed_roles", "photo")}),
        ("About", {"fields": ("about",)}),
        ("Contact", {"fields": ("email", "phone", "location", "github_username", "linkedin_url")}),
        ("Files", {"fields": ("resume",)}),
        ("Flags", {"fields": ("available_for_work", "is_active")}),
    )


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ("name", "proficiency", "is_featured", "order")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "skill_count", "order")
    list_editable = ("order",)
    inlines = [SkillInline]

    @admin.display(description="Skills")
    def skill_count(self, obj):
        return obj.skills.count()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("name",)
    list_editable = ("proficiency", "is_featured", "order")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "period", "score", "order")
    list_editable = ("order",)
    search_fields = ("institution", "degree")


class ExperienceBulletInline(admin.TabularInline):
    model = ExperienceBullet
    extra = 2


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organisation", "period", "order")
    list_editable = ("order",)
    inlines = [ExperienceBulletInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "badge", "is_featured", "order", "links")
    list_filter = ("category", "is_featured")
    list_editable = ("is_featured", "order")
    search_fields = ("title", "short_description", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basics", {"fields": ("title", "slug", "subtitle", "category", "badge")}),
        ("Content", {"fields": ("short_description", "description", "highlights", "tech_stack")}),
        ("Media & links", {"fields": ("image", "github_url", "live_url")}),
        ("Display", {"fields": ("is_featured", "order")}),
    )

    @admin.display(description="Links")
    def links(self, obj):
        parts = []
        if obj.github_url:
            parts.append(f'<a href="{obj.github_url}" target="_blank">code</a>')
        if obj.live_url:
            parts.append(f'<a href="{obj.live_url}" target="_blank">live</a>')
        return format_html(" · ".join(parts)) if parts else "—"


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "issuer", "period", "order")
    list_filter = ("kind",)
    list_editable = ("order",)
    search_fields = ("title", "issuer")


@admin.register(CodingProfile)
class CodingProfileAdmin(admin.ModelAdmin):
    list_display = ("platform", "username", "stat_value", "order")
    list_editable = ("order",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order")
    list_editable = ("level", "order")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    actions = ["mark_read", "mark_unread"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected messages as read")
    def mark_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.")

    @admin.action(description="Mark selected messages as unread")
    def mark_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.")
