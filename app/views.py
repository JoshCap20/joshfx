from django.shortcuts import render
from django.db.models import Q
from app.models import Movie

def stream(request, query):
  movie = Movie.objects.get(id=query)
  return movie.stream_external_video()

def index(request):
  query = request.GET.get('q', '')
  type = request.GET.get('type', 'all')
  if query:
      if type == "all":
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query))
      else:
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query)).filter(type=type)
  else:
      if type == "all":
        movies = Movie.objects.all()
      else:
        movies = Movie.objects.filter(type=type)
  return render(request, 'index.html', {'movies': movies})