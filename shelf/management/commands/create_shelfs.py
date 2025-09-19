from django.core.management.base import BaseCommand

from shelf.models import Shelf,NumOfBooks

class Command(BaseCommand):
    help = "Creating shelfs...!"

    def handle(self, *args, **kwargs):
        stages = ['A','B','C']
        for col in range(1,8,1):
            col = str(col)
            for rac in range(1,6,1):
                rac = str(rac)
                for stage in range(1,4,1):
                    stage=str(stage)
                    for i in ['A','B','C']:
                        addr = "C"+col+'-R'+rac+'-'+i+stage
                        shelf = Shelf.objects.create(Address=addr,Quantity=NumOfBooks.ZERO)
                        
                        self.stdout.write(f"Address '{addr}' is addes to Shelf(database)...:) {shelf}")
        pass