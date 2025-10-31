import uuid
from shelf.models import Shelf,NumOfBooks
from django.utils.text import slugify
from django.db import models

from users.models import CustomUser
from django.core.exceptions import ValidationError



def validate_book_addr(value):
    inst = Shelf.objects.get(addr=value)
    if inst.qunt >=5 :
        raise ValidationError('that shelf was full')
def validate_catagory(value):
    if value=="":
        raise ValidationError("Catagory should not be empty")
def generate_uuid_hex():
    return uuid.uuid4().hex

# Create your models here.
class bookTag(models.Model):
    name = models.CharField(max_length=100,unique=True,help_text="Tag Name",primary_key=True,db_index=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower().replace(" ", "_")
        super().save(*args, **kwargs)



class Book(models.Model):
    id = models.CharField(max_length=100,default=generate_uuid_hex,unique=True,primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    catagory = models.ManyToManyField(bookTag)
    addr = models.ForeignKey(Shelf,on_delete=models.CASCADE,validators=[validate_book_addr])
    slug = models.SlugField(unique=True, blank=True)
    discription = models.TextField(null=True,blank=True,)
    auther = models.CharField(max_length=50,default="Not defined")
    class Meta:
        unique_together = ("name", "auther")

    def delete(self, *args, **kwargs):
        if self.addr.qunt > 0:
            inst = Shelf.objects.get(addr=self.addr)
            inst.qunt = self.addr.qunt - 1
            inst.save()
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.addr.qunt < 5:
            inst = Shelf.objects.get(addr=self.addr)
            inst.qunt = self.addr.qunt + 1
            inst.save()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class issueBook(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    issued_on = models.DateField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return self.book.name + " is issued to " + str(self.user)