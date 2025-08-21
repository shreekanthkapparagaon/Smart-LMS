from django.db import models
from users.models import CustomUser
import datetime

# Create your models here.
class LogEntries(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    entered_at = models.DateTimeField(default=lambda:datetime.datetime.now())
    exited_at = models.DateTimeField(null=True, blank=True)

    def duration(self):
        if self.entered_at and self.exited_at:
            return self.exited_at - self.entered_at
        return None

    def __str__(self):
        return f" {self.user} is visited from {self.entered_at} to {self.exited_at} "