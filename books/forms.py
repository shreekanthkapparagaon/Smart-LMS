from django import forms
from django.contrib import admin
from .models import Book
from django.templatetags.static import static


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
        }
    def clean_name(self):
                quantity = self.cleaned_data['name']
                if quantity is None:
                    raise forms.ValidationError("Name field should not be None...!")
                return quantity
    class Media:
        js = [static("js/main.js")]