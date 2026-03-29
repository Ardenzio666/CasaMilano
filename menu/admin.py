from django.contrib import admin
from .models import Menu, MenuCourse

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MenuCourse)
class MenuCourseAdmin(admin.ModelAdmin):
    list_display = ('menu','title')
