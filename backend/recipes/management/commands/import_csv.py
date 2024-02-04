import csv

from django.core.management import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    def import_ingredients(self):
        with open('/data/ingredients.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Ingredients.objects.create(
                    name=row['name'], measurement_unit=row['measurement_unit']
                )

    def handle(self, *args, **options):
        self.import_ingredients()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
