import uuid
from shelf.models import Shelf,NumOfBooks
from django.utils.text import slugify
from django.db import models

from users.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.
class bookCategory(models.Model):
    name = models.CharField(max_length=100,unique=True,default='null',primary_key=True,db_index=True)
    def __str__(self):
        return self.name
def validate_book_addr(value):
    inst = Shelf.objects.get(Address=value)
    if inst.Quantity >=5 :
        raise ValidationError('that shelf was full')
def validate_catagory(value):
    if value=="":
        raise ValidationError("Catagory should not be empty")
def generate_uuid_hex():
    return uuid.uuid4().hex

class Book(models.Model):
    id = models.CharField(max_length=100,default=generate_uuid_hex,unique=True,primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    catagory = models.ForeignKey(bookCategory,on_delete=models.CASCADE,validators=[validate_catagory],db_index=True)
    addr = models.ForeignKey(Shelf,on_delete=models.CASCADE,default='NA',validators=[validate_book_addr],db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    discription = models.TextField(null=True,blank=True,)
    auther = models.CharField(max_length=50,default="Not defined")
    def delete(self, *args, **kwargs):
        if self.addr.Quantity > 0:
            inst = Shelf.objects.get(Address=self.addr)
            inst.Quantity = self.addr.Quantity - 1
            inst.save()
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.addr.Quantity < 5:
            inst = Shelf.objects.get(Address=self.addr)
            inst.Quantity = self.addr.Quantity + 1
            inst.save()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class issueBook(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    def delete(self, *args, **kwargs):
        inst = Shelf.objects.get(Address=self.book.addr)
        inst.Quantity = self.book.addr.Quantity - 1
        returned_shef = Shelf.objects.filter(Address='On Table').first()
        if not returned_shef:
            returned_shef = Shelf(Address='On Table')
            returned_shef.save()
        returned_shef.save()
        bookIst = Book.objects.get(id=self.book.id)
        returned_shef = Shelf.objects.filter(Address='On Table').first()
        if not returned_shef:
            returned_shef = Shelf(Address='On Table')
            returned_shef.save()
        bookIst.addr = returned_shef
        bookIst.save()
        inst.save()
        print(self.book.addr)
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        inst = Shelf.objects.get(Address=self.book.addr)
        inst.Quantity = self.book.addr.Quantity - 1
        returned_shef = Shelf.objects.filter(Address='Issued').first()
        if not returned_shef:
            returned_shef = Shelf(Address='Issued')
            returned_shef.save()
        returned_shef.save()
        bookIst = Book.objects.get(id=self.book.id)
        returned_shef = Shelf.objects.filter(Address='Issued').first()
        if not returned_shef:
            returned_shef = Shelf(Address='Issued')
            returned_shef.save()
        bookIst.addr = returned_shef
        bookIst.save()
        inst.save()


        super().save(*args, **kwargs)
    def __str__(self):
        return self.book.name + " is issued to " + str(self.user)