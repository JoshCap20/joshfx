from django.contrib import admin

from app.models import Movie, Request

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

make_inactive.short_description = "Mark selected movies as inactive"

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'source', 'active')
    list_per_page = 300
    search_fields = ('title', 'type', 'path', 'source')
    ordering = ('title',)
    list_filter = ('type', 'source', 'active')
    actions = [make_inactive]

class RequestAdmin(admin.ModelAdmin):
    list_display = ('info', 'date', 'count')
    list_per_page = 300
    search_fields = ('info', 'date', 'count')
    ordering = ('date',)
    list_filter = ('date', 'count')

admin.site.register(Request, RequestAdmin)

admin.site.register(Movie, MovieAdmin)
