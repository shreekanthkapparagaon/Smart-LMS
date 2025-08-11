# signals.py
from django.db.models.signals import post_save
from .models import Profile,CustomUser

# @receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile=Profile(user=instance)
        profile.save()
#
# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

post_save.connect(create_profile,sender=CustomUser)
