from django.contrib import admin

from app.models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'source')
    list_per_page = 300
    search_fields = ('title', 'type', 'path', 'source')
    ordering = ('title',)
    list_filter = ('type', 'source')


admin.site.register(Movie, MovieAdmin)
