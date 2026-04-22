from django.contrib import admin
from .models import Menu, MenuCourse

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
