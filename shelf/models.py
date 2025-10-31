from django.db import models

# Create your models here.
class NumOfBooks(models.IntegerChoices):
    ZERO = 0, '0'
    FIRST = 1, '1'
    SECOND = 2, '2'
    THIRD = 3, '3'
    FOURTH = 4, '4'
    FIFTH = 5, '5'
    # ... other fields
class Shelf(models.Model):
    addr = models.CharField("Address",max_length=10,primary_key=True,db_index=True)
    qunt = models.IntegerField("Quantity",default=0)

    def __str__(self):
        return self.addr