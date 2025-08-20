from django.db import models
from django.utils.text import slugify
from users.models import CustomUser
from tinymce.models import HTMLField
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    discription = HTMLField(null=True,blank=True)
    auther = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)