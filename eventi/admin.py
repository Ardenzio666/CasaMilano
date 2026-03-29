from django.contrib import admin
from .models import Event

@admin.register(Event)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','is_published')
    prepopulated_fields = {'slug': ('title',)}
