from django.contrib import admin

from app.models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'link')

admin.site.register(Movie, MovieAdmin)