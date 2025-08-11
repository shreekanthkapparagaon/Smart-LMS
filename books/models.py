import uuid

from django.utils.text import slugify
from django.db import models

from users.models import CustomUser


# Create your models here.
class bookCategory(models.Model):
    name = models.CharField(max_length=100,unique=True,default='null',primary_key=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.CharField(max_length=100,default=uuid.uuid4().hex,unique=True,primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    catagory = models.ForeignKey(bookCategory,on_delete=models.CASCADE,default='null')
    slug = models.SlugField(unique=True, blank=True)
    discription = models.TextField(null=True,blank=True,default="i am a discription")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class issueBook(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name + " is issued to " + str(self.user)