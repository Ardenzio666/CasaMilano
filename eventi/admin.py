from django.contrib import admin
from .models import Event, EventComment, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(Event)
class MenuAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ('title','is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "text", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("text", "event__title", "user__username")
    readonly_fields = ("created_at",)
