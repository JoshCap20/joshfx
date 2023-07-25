from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View

from app.models import Movie

#############################################
#          Website Views and APIS           #
#############################################


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class SearchAPI(View):
    def get(self, request):
        query = request.GET.get('q', '')
        type = request.GET.get('type', 'all')
        source = request.GET.get('source', 'all')
        media = request.GET.get('media', 'all')

        if query:
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(path__icontains=query))
        else:
            if type != "all" or source != "all" or media != "all":
                movies = Movie.objects.all()
            else:
                movies = Movie.objects.filter(title__icontains="family guy")

        if type != "all":
            movies = movies.filter(type=type)
        if source != "all":
            movies = movies.filter(source=source)
        if media != "all":
            movies = movies.filter(path__icontains=media)

        return JsonResponse([mov.json() for mov in movies], safe=False)


def stream(request, query):
    if not query.isdigit() or not query:
        return HttpResponseNotFound("Movie not found")
    try:
        movie = Movie.objects.get(id=query)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Movie not found")
    return movie.stream_external_video_adv(request)
