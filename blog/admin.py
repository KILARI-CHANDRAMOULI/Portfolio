from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "post_count")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Posts")
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at", "reading_minutes", "views")
    list_filter = ("status", "category", "published_at")
    search_fields = ("title", "excerpt", "body", "tags")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    readonly_fields = ("views", "created_at", "updated_at")
    actions = ["publish", "unpublish"]
    fieldsets = (
        ("Basics", {"fields": ("title", "slug", "category", "tags")}),
        ("Content", {"fields": ("excerpt", "body", "cover_image")}),
        ("Publishing", {"fields": ("status", "published_at", "reading_minutes")}),
        ("Stats", {"fields": ("views", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.action(description="Publish selected posts")
    def publish(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED)

    @admin.action(description="Move selected posts to draft")
    def unpublish(self, request, queryset):
        queryset.update(status=Post.Status.DRAFT)
