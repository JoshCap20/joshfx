from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from app.models import Movie
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from asgiref.sync import sync_to_async

async def stream(request, query):
  try:
    movie = await sync_to_async(Movie.objects.get(id=query))
  except Movie.DoesNotExist:
    return HttpResponseNotFound("Movie not found")
  return movie.stream_external_video_adv(request)
    
async def index(request):
  query = request.GET.get('q', '')
  type = request.GET.get('type', 'all')
  source = request.GET.get('source', 'all')
  media = request.GET.get('media', 'all')
  
  if query:
    movies = await sync_to_async(Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query)))
  else:
    movies = await sync_to_async(Movie.objects.all())

  if type != "all":
    movies = await sync_to_async(movies.filter(type=type))
  if source != "all":
    movies = await sync_to_async(movies.filter(source=source))
  if media != "all":
    movies = await sync_to_async(movies.filter(path__icontains=media))

  return render(request, 'index.html', {'movies': movies})

#############################################
#                 TV APIs                   #
#############################################

async def get_link(request):
    # If query is not a number, look up title
    query = request.GET.get('q', '')

    if query.isdigit():
        movie = await sync_to_async(get_object_or_404(Movie, id=query))
    else:
        movie = await sync_to_async(Movie.objects.filter(title__icontains=query).first())
    
    if movie:
        # movie.link is a URL to the video file
        return HttpResponseRedirect(movie.link, status=302)
    else:
        return HttpResponseNotFound("No movie found")

async def get_results(request):
    # If query is not a number, look up title
    query = request.GET.get('q', '')

    movie = await sync_to_async(Movie.objects.filter(title__icontains=query).only('id', 'title', 'link'))
    
    if movie:
      # movie.link is a URL to the video file
      return JsonResponse([mov.json() for mov in movie], safe=False)
    else:
      return HttpResponseNotFound("No movie found")