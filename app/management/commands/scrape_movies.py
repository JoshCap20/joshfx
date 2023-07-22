from django.core.management.base import BaseCommand
from scripts.parser import Scraper as scraper

class Command(BaseCommand):
    help = 'Scrapes movies into a CSV file'

    def handle(self, *args, **kwargs):
        scraper.scrape()
        self.stdout.write(self.style.SUCCESS('Movies scraped successfully'))
