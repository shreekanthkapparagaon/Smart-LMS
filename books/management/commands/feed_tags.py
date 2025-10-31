import json
from django.core.management.base import BaseCommand
from books.models import bookTag


class Command(BaseCommand):
    help = "Import tags from a JSON file and create them if they do not exist."

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing tag names')

    def handle(self, *args, **options):
        json_file = options['json_file']
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to read JSON file: {e}"))
            return

        # Handle both {"tags": [...]} and plain list formats
        tags = data.get("tags") if isinstance(data, dict) else data

        exist_count = 0
        created_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING(f"📦 Loading {len(tags)} tags...\n"))

        for tag_name in tags:
            tag, created = bookTag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added new tag: {tag_name}"))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Tag already exists: {tag_name}"))
                exist_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n✅ {created_count} new tags created."))
        self.stdout.write(self.style.WARNING(f"⚠️ {exist_count} tags already existed."))
