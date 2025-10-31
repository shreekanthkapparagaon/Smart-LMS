from django.core.management.base import BaseCommand
from shelf.models import Shelf

class Command(BaseCommand):
    help = "Bulk-create shelf entries using Z{zone}-R{rack}-L{level} format"

    def add_arguments(self, parser):
        parser.add_argument('--zones', type=int, default=7)
        parser.add_argument('--racks', type=int, default=8)
        parser.add_argument('--levels', type=int, default=5)

    def handle(self, *args, **options):
        zones, racks, levels = options['zones'], options['racks'], options['levels']
        shelf_list = [
            Shelf(addr=f"Z{z}-R{r}-L{l}", qunt=0)
            for z in range(1, zones + 1)
            for r in range(1, racks + 1)
            for l in range(1, levels + 1)
        ]
        Shelf.objects.bulk_create(shelf_list, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"{len(shelf_list)} shelf entries attempted for creation."))