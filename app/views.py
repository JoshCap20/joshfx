from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from app.models import Movie

def stream(request, query):
  movie = Movie.objects.get(id=query)
  # if movie.type == "mkv":
  #   return stream_mkv(request, query)
  return movie.stream_external_video()

def stream_mkv(request, query):
  movie = Movie.objects.get(id=query)
  return render(request, 'mkv.html', {'movie': movie})

from django.http import HttpResponseNotFound, HttpResponseRedirect

def get_link(request, query):
    # If query is not a number, look up title
    if query.isdigit():
        movie = get_object_or_404(Movie, id=query)
    else:
        movie = Movie.objects.filter(title__icontains=query, type="mp4").first()
    
    if movie:
        # movie.link is a URL to the video file
        return HttpResponseRedirect(movie.link, status=302)
    else:
        return HttpResponseNotFound("No movie found")
    
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