import json
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from books.models import Book, bookTag
from shelf.models import Shelf


class Command(BaseCommand):
    help = "Fast import of books (bulk insert) and auto-assign to shelves, with slug fix."

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error reading JSON: {e}"))
            return

        self.stdout.write(self.style.NOTICE(f"📚 Starting optimized import of {len(books_data)} books...\n"))

        # ----------------------------------------------------
        # CACHE shelves & tags
        # ----------------------------------------------------
        shelves = list(Shelf.objects.all())  # include all shelves
        if not shelves:
            self.stderr.write(self.style.ERROR("❌ No shelves found. Please create some first."))
            return

        tag_cache = {t.name: t for t in bookTag.objects.all()}
        shelf_capacity = {s.pk: Book.objects.filter(addr=s).count() for s in shelves}

        new_tags = []
        new_books = []
        book_tag_relations = []

        # ----------------------------------------------------
        # Generate books
        # ----------------------------------------------------
        for entry in books_data:
            title = entry.get("title")
            author = entry.get("author", "Not defined")
            description = entry.get("description", "")
            tag_names = entry.get("tags list", [])

            # Skip duplicates
            if Book.objects.filter(name=title, auther=author).exists():
                continue

            # Cache tags
            tags = []
            for name in tag_names:
                tag = tag_cache.get(name)
                if not tag:
                    tag = bookTag(name=name)
                    tag_cache[name] = tag
                    new_tags.append(tag)
                tags.append(tag)

            # Find available shelf (<5 books)
            shelf = self._find_shelf(shelves, shelf_capacity)
            if not shelf:
                self.stderr.write(self.style.WARNING(f"No shelf space left for '{title}', skipping."))
                continue
            shelf_capacity[shelf.pk] += 1

            # ✅ Generate unique slug
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists() or any(b.slug == slug for b in new_books if hasattr(b, "slug")):
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Prepare Book object
            book = Book(
                name=title,
                auther=author,
                discription=description,
                addr=shelf,
                slug=slug  # 👈 Important
            )
            new_books.append(book)
            book_tag_relations.append((book, tags))

        # ----------------------------------------------------
        # Bulk create tags + books
        # ----------------------------------------------------
        with transaction.atomic():
            if new_tags:
                bookTag.objects.bulk_create(
                    [t for t in new_tags if not t.pk],
                    ignore_conflicts=True
                )
                self.stdout.write(self.style.SUCCESS(f"🆕 Created {len(new_tags)} new tags."))

            Book.objects.bulk_create(new_books)
            self.stdout.write(self.style.SUCCESS(f"📗 Bulk-inserted {len(new_books)} books."))

            # Refresh tag cache
            tag_cache = {t.name: t for t in bookTag.objects.all()}

            # Add M2M tags
            for book, tags in book_tag_relations:
                tag_objs = [tag_cache[t.name] for t in tags if t.name in tag_cache]
                book.catagory.add(*tag_objs)

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING("\n📦 IMPORT SUMMARY 📦"))
        self.stdout.write(self.style.SUCCESS(f"✅ Books created: {len(new_books)}"))
        self.stdout.write(self.style.SUCCESS(f"🏷️  Tags used: {len(tag_cache)}"))
        self.stdout.write(self.style.NOTICE(f"📘 Total processed: {len(books_data)}"))


    # --------------------------------------------------------
    # Helper: find available shelf with <5 books
    # --------------------------------------------------------
    def _find_shelf(self, shelves, shelf_capacity, max_per_shelf=20):
        for shelf in shelves:
            if shelf_capacity.get(shelf.pk, 0) < max_per_shelf:
                return shelf
        return None
