from django.contrib import admin
from .models import DishComment, Menu, MenuCourse

from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_published', 'is_featured')
    list_editable = ('order', 'is_published', 'is_featured')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'short_description', 'description')
    list_filter = ('is_published', 'is_featured')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MenuCourse)
class MenuCourseAdmin(admin.ModelAdmin):
    list_display = ('menu','title')

@admin.register(DishComment)
class DishCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "dish", "user", "text", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("text", "dish__title", "user__username")
    readonly_fields = ("created_at",)
