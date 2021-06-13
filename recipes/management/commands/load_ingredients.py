import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load ingredients from json file'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, path: str, **options):
        with open(path[0]) as file:
            for item in json.load(file):
                Ingredient.objects.get_or_create(
                    title=item['title'],
                    dimension=item['dimension'],
                )
        print('Loaded successfully!')
