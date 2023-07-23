from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from app.models import Movie
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse

def stream(request, query):
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
    movies = Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query))
  else:
    movies = Movie.objects.all()

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
    query = request.GET.get('q', '')

    if query.isdigit():
        movie = get_object_or_404(Movie, id=query)
    else:
        movie = Movie.objects.filter(title__icontains=query).first()
    
    if movie:
        # movie.link is a URL to the video file
        return HttpResponseRedirect(movie.link, status=302)
    else:
        return HttpResponseNotFound("No movie found")

def get_results(request):
    # If query is not a number, look up title
    query = request.GET.get('q', '')

    movie = Movie.objects.filter(title__icontains=query).only('id', 'title', 'link')
    
    if movie:
      # movie.link is a URL to the video file
      return JsonResponse([mov.json() for mov in movie], safe=False)
    else:
      return HttpResponseNotFound("No movie found")