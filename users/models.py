from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager
import uuid

def generate_uuid_hex():
    return uuid.uuid4().hex

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True,default=generate_uuid_hex,editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_user = models.AutoField(primary_key=True)
    bio = models.TextField(blank=True, default='')
    profileimg = models.ImageField(upload_to='profile_images', default='default-avtar.png')
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.email