from django.shortcuts import render
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

def index(request):
  query = request.GET.get('q', '')
  type = request.GET.get('type', 'all')
  source = request.GET.get('source', 'all')
  
  if query:
    movies = Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query))
  else:
    movies = Movie.objects.all()
  if type != "all":
    movies = movies.filter(type=type)
  if source != "all":
    movies = movies.filter(source=source)
  return render(request, 'index.html', {'movies': movies})