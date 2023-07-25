from django.contrib import admin

from app.models import Movie, Request


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'source')
    list_per_page = 300
    search_fields = ('title', 'type', 'path', 'source')
    ordering = ('title',)
    list_filter = ('type', 'source')

class RequestAdmin(admin.ModelAdmin):
    list_display = ('info', 'date', 'count')
    list_per_page = 300
    search_fields = ('info', 'date', 'count')
    ordering = ('date',)
    list_filter = ('date', 'count')

admin.site.register(Request, RequestAdmin)

admin.site.register(Movie, MovieAdmin)
