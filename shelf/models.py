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
    addr = models.CharField(max_length=10,name='Address',primary_key=True,db_index=True)
    qunt = models.IntegerField(choices=NumOfBooks.choices, default=NumOfBooks.ZERO,name='Quantity')

    def __str__(self):
        return self.Address