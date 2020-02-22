from django.contrib import admin
from .models import Resource

# Register your models here.
<<<<<<< HEAD
=======


class ResourceAdmin(admin.ModelAdmin):

    list_display = ['tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

>>>>>>> d57b07986d5c3e64b97c59609e3bb972d01411aa
admin.site.register(Resource)
