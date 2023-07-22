from django.core.management.base import BaseCommand
from app.models import Movie

class Command(BaseCommand):
    help = 'Clears the database'

    def handle(self, *args, **kwargs):
        Movie.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Database cleared successfully'))
