from django.db.models import Q
from django.http import (HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, render

from app.models import Movie


def stream(request, query):
    if not query.isdigit() or query is None:
        return HttpResponseNotFound("Movie not found")
    try:
        movie = Movie.objects.get(id=query)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Movie not found")
    return movie.stream_external_video_adv(request)


def index(request):
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

    return render(request, 'index.html', {'movies': movies})

#############################################
#                 TV APIs                   #
#############################################


def get_link(request):
    # If query is not a number, look up title
    query = request.GET.get('q', None)

    if query is None:
        return HttpResponseNotFound("No query provided")

    if query.isdigit():
        movie = get_object_or_404(Movie, id=query)
    else:
        movie = Movie.objects.filter(title__icontains=query).first()

    if movie:
        return HttpResponseRedirect(movie.link, status=302)
    else:
        return HttpResponseNotFound("No movie found")


def get_results(request):
    # If query is not a number, look up title
    query = request.GET.get('q', None)

    if query is None:
        return HttpResponseNotFound("No query provided")

    movie = Movie.objects.filter(
        title__icontains=query).only('id', 'title', 'link')

    if movie:
        return JsonResponse([mov.json() for mov in movie], safe=False)
    else:
        return HttpResponseNotFound("No movie found")
