from django.core.paginator import Paginator
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
    MOVIES_PER_PAGE: int = 200

    def get(self, request):
        query = request.GET.get('q', 'all')
        type = request.GET.get('type', 'all')
        source = request.GET.get('source', 'all')
        media = request.GET.get('media', 'all')

        if query != "all":
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(path__icontains=query))
        else:
            movies = Movie.objects.all()
            
        if type != "all":
            movies = movies.filter(type=type)
        if source != "all":
            movies = movies.filter(source=source)
        if media != "all":
            movies = movies.filter(path__icontains=media)

        paginator = Paginator(movies, self.MOVIES_PER_PAGE)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        movies = list(page_obj.object_list.values('id', 'title', 'link', 'source', 'type', 'path'))

        return JsonResponse({"movies":movies, "page":page_number, "pages":paginator.num_pages, "total":paginator.count})


def stream(request, query):
    if not query.isdigit() or not query:
        return HttpResponseNotFound("Movie not found")
    try:
        movie = Movie.objects.get(id=query)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Movie not found")
    return movie.stream_external_video_adv(request)
