import json
from django.core.management.base import BaseCommand
from books.models import Shelf

class Command(BaseCommand):
    help = "Load shelves from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        added = 0
        for entry in data:
            address = entry.get("Address")
            quantity = entry.get("Quantity")

            if not address or quantity is None:
                self.stderr.write(self.style.WARNING(f"Skipping invalid entry: {entry}"))
                continue

            shelf, created = Shelf.objects.get_or_create(Address=address)
            if not created:
                shelf.Quantity = int(quantity)
                shelf.save()
            added += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {added} shelves from {json_file}"))