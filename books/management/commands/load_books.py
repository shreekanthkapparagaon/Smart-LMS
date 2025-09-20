import json
from django.core.management.base import BaseCommand
from books.models import Book, bookCategory, Shelf

class Command(BaseCommand):
    help = "Load books from a JSON file"

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
        failed = 0

        for entry in data:
            name = entry.get("name")
            auther = entry.get("auther")
            slug = entry.get("slug")
            cat_name = entry.get("catagory__name")
            shelf_addr = entry.get("addr__Address")

            if not all([name, auther, slug, cat_name, shelf_addr]):
                self.stderr.write(self.style.WARNING(f"Skipping incomplete entry: {entry}"))
                failed += 1
                continue

            category,BookCreated = bookCategory.objects.get_or_create(name=cat_name)
            shelf,ShelfCreated = Shelf.objects.get_or_create(Address=shelf_addr)

            if BookCreated:
                self.stderr.write(self.style.SUCCESS(f"Book category created with {category}.."))
            if ShelfCreated:
                self.stderr.write(self.style.SUCCESS(f"Book category created with {shelf}.."))
            if not category or not shelf:
                self.stderr.write(self.style.WARNING(f"Invalid category or shelf for: {name}"))
                failed += 1
                continue

            book, created = Book.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "auther": auther,
                    "catagory": category,
                    "addr": shelf
                }
            )

            if created:
                added += 1
            else:
                self.stderr.write(self.style.WARNING(f"Book already exists: {slug}"))
                failed += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Added {added} books"))
        self.stdout.write(self.style.WARNING(f"❌ Skipped {failed} entries"))