
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "seed database with default template"


    def handle(self, *args, **options):
        print('Works')