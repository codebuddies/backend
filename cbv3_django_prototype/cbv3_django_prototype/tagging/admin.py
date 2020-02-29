from django.contrib import admin
from resources.models import TaggedItems
from .models import CustomTag



class TaggedItemInline(admin.StackedInline):
    model = TaggedItems


@admin.register(CustomTag)
class TagsAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["guid", "name", "slug"]
    ordering = ["name", "slug", "guid"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
