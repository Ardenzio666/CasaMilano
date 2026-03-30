from django.contrib import admin
from .models import Event, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(Event)
class MenuAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ('title','is_published')
    prepopulated_fields = {'slug': ('title',)}
