from django.contrib import admin
from .models import Hangout, HangoutSessions, HangoutResponses

# Register your models here.
class HangoutSessionsInline(admin.StackedInline):
    model = HangoutSessions
    readonly_fields = ('id', 'guid')


class HangoutResponsesInline(admin.StackedInline):
    model = HangoutResponses
    readonly_fields = ('id', 'guid')


class HangoutAdmin(admin.ModelAdmin):
    model = Hangout
    readonly_fields = ('id', 'guid')
    list_display = ['tag_list']
    inlines = ['HangoutSessionsInline', 'HangoutResponsesInline']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Hangout)
admin.site.register(HangoutResponses)
admin.site.register(HangoutSessions)
