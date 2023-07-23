from django.shortcuts import render
from django.db.models import Q
from app.models import Movie

def stream(request, query):
  movie = Movie.objects.get(id=query)
  return movie.stream_external_video()

def index(request):
  query = request.GET.get('q', '')
  if query:
      movies = Movie.objects.filter(Q(title__icontains=query) | Q(path__icontains=query))
  else:
      movies = Movie.objects.all()
  return render(request, 'index.html', {'movies': movies})