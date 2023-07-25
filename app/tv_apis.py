from django.http import (HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404

from app.models import Movie

#############################################
#                 TV APIs                   #
#############################################


def get_link(request):
    query = request.GET.get('q', None)

    if not query:
        return HttpResponseNotFound("No query provided")

    if query.isdigit():
        movie = get_object_or_404(Movie, id=query)
    else:
        movie = Movie.objects.filter(title__icontains=query).first()

    if not movie:
        return HttpResponseNotFound("No movie found")
    return HttpResponseRedirect(movie.link, status=302)


def get_results(request):
    query = request.GET.get('q', None)

    if not query:
        return HttpResponseNotFound("No query provided")

    movie = Movie.objects.filter(
        title__icontains=query).only('id', 'title', 'link')

    if not movie:
        return HttpResponseNotFound("No movie found")
    return JsonResponse([mov.json() for mov in movie], safe=False)
