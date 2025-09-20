from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from django.templatetags.static import static


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
    class Media:
        js = [static("js/main.js")]
