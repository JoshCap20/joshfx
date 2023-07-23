from django.core.management.base import BaseCommand
from app.models import Movie
import csv
import os.path

class Command(BaseCommand):
    help = 'Loads movies from a CSV file into the database'

    sources = {
        "http://102.212.178.1:8089/": 1,
        "http://185.223.160.51/": 2,
        "http://192.121.102.206/": 3,
        "http://92.247.236.71:9800/": 4,
        "http://66.242.75.177/": 5,
        "http://195.154.237.18:9000/": 6,
        "http://210.54.35.157:9000/": 7,
        "http://124.184.68.140/": 8,
        "http://195.154.108.130:9000/": 9,
        "http://120.28.137.252/": 10,
        "http://144.137.208.140:9000/": 11,
        "http://72.253.204.218:9999/movies/": 12,
        "http://96.233.113.244/": 13,
        "http://23.147.64.113/": 14,
    }

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File "{csv_file}" does not exist'))
            return

        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                title, link, source, path = row
                if '%27' in title:
                    title = title.replace('%27', "'")
                elif '%20' in title:
                    title = title.replace('%20', ' ')
                type = 'mp4' if link.endswith('.mp4') else 'mkv'
                source = self.sources[source]
                Movie.objects.get_or_create(title=title, type=type, link=link, source=source, path=path)

        self.stdout.write(self.style.SUCCESS('Movies loaded successfully'))
